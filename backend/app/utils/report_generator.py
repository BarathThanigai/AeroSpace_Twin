import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from ..core.incident_manager import IncidentManager


class ReportGenerator:
    """Generate incident reports in JSON and optionally PDF format."""

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_json_report(
        self,
        incident_manager: IncidentManager,
        aircraft_state: Dict[str, Any],
        threat_confidence: float,
    ) -> Dict:
        """Generate incident report as JSON."""

        incident = incident_manager.get_current_incident()

        if not incident:
            return {"error": "No active incident"}

        duration = 0
        if incident.get("resolution_time"):
            start = datetime.fromisoformat(incident["start_time"])
            end = datetime.fromisoformat(incident["resolution_time"])
            duration = (end - start).total_seconds()

        report = {
            "incident_id": incident["incident_id"],
            "timestamp": datetime.now().isoformat(),
            "threat_type": incident["threat_type"],
            "confidence_score": incident["threat_confidence"],
            "affected_systems": incident["affected_subsystems"],
            "current_risk": incident["current_risk"],
            "predicted_impact": {
                "risk_score": incident["predicted_risk"],
                "timeline_stage": incident["timeline_stage"],
            },
            "recommended_actions": [r.get("action", r) for r in incident["recommendations"]],
            "applied_mitigations": incident["applied_mitigations"],
            "final_risk_assessment": incident.get("final_risk", incident["current_risk"]),
            "duration_seconds": duration,
            "aircraft_state": aircraft_state,
        }

        return report

    def save_report(self, report: Dict, filename: Optional[str] = None) -> str:
        """Save report to JSON file."""
        if not filename:
            filename = f"incident_{report['incident_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        filepath = self.output_dir / filename
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)

        return str(filepath)

    def generate_pdf_report(self, report: Dict, filename: Optional[str] = None) -> Optional[str]:
        """Generate PDF report (optional, requires ReportLab)."""
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib import colors

            if not filename:
                filename = f"incident_{report['incident_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

            filepath = self.output_dir / filename

            doc = SimpleDocTemplate(str(filepath), pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            # Title
            title_style = ParagraphStyle(
                "CustomTitle",
                parent=styles["Heading1"],
                fontSize=24,
                textColor=colors.HexColor("#FF6B6B"),
                spaceAfter=30,
            )
            title = Paragraph(f"AeroShield Twin - Incident Report", title_style)
            elements.append(title)

            # Incident Details
            incident_data = [
                ["Field", "Value"],
                ["Incident ID", report.get("incident_id", "N/A")],
                ["Threat Type", report.get("threat_type", "N/A")],
                ["Confidence", f"{report.get('confidence_score', 0):.1f}%"],
                ["Timestamp", report.get("timestamp", "N/A")],
                ["Initial Risk", f"{report.get('current_risk', 0)}%"],
                ["Final Risk", f"{report.get('final_risk_assessment', 0)}%"],
                ["Duration", f"{report.get('duration_seconds', 0):.1f}s"],
            ]

            incident_table = Table(incident_data, colWidths=[2 * inch, 3 * inch])
            incident_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )
            elements.append(incident_table)
            elements.append(Spacer(1, 0.3 * inch))

            # Affected Systems
            heading = Paragraph("Affected Systems", styles["Heading2"])
            elements.append(heading)
            affected = ", ".join(report.get("affected_systems", []))
            elements.append(Paragraph(affected, styles["Normal"]))
            elements.append(Spacer(1, 0.2 * inch))

            # Recommendations
            heading = Paragraph("Recommended Actions", styles["Heading2"])
            elements.append(heading)
            for action in report.get("recommended_actions", []):
                elements.append(Paragraph(f"• {action}", styles["Normal"]))
            elements.append(Spacer(1, 0.2 * inch))

            # Applied Mitigations
            heading = Paragraph("Applied Mitigations", styles["Heading2"])
            elements.append(heading)
            mitigations = report.get("applied_mitigations", [])
            if mitigations:
                for mitigation in mitigations:
                    elements.append(Paragraph(f"• {mitigation}", styles["Normal"]))
            else:
                elements.append(Paragraph("No mitigations applied", styles["Normal"]))

            doc.build(elements)
            return str(filepath)

        except ImportError:
            print("ReportLab not installed. Skipping PDF generation.")
            return None
