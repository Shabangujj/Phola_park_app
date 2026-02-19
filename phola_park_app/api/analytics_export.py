from flask import Blueprint, Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from sqlalchemy import func
from datetime import datetime
import csv
from io import StringIO, BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from phola_park_app.model import Report
from phola_park_app.api.analytics import apply_date_filters

analytics_export_api = Blueprint(
    "analytics_export_api",
    __name__,
    url_prefix="/analytics/export"
)
def analytics_base_query():
    claims = get_jwt()
    role = claims.get("role")
    portfolio = claims.get("portfolio")

    query = Report.query

    # supervisor sees only their portfolio
    if role == "supervisor":
        query = query.filter_by(portfolio=portfolio)

    query = apply_date_filters(query, Report.created_at)
    return query
@analytics_export_api.route("/csv", methods=["GET"])
@jwt_required()
def export_analytics_csv():
    claims = get_jwt()

    if claims.get("role") not in ["admin", "supervisor"]:
        return jsonify({"error": "Unauthorized"}), 403

    query = analytics_base_query()

    results = (
        query
        .with_entities(
            Report.category,
            Report.status,
            Report.portfolio,
            func.count(Report.id)
        )
        .group_by(Report.category, Report.status, Report.portfolio)
        .all()
    )

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Category",
        "Status",
        "Portfolio",
        "Count"
    ])

    for row in results:
        writer.writerow(row)

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = (
        "attachment; filename=analytics_report.csv"
    )

    return response
@analytics_export_api.route("/pdf", methods=["GET"])
@jwt_required()
def export_analytics_pdf():
    claims = get_jwt()

    if claims.get("role") not in ["admin", "supervisor"]:
        return jsonify({"error": "Unauthorized"}), 403

    query = analytics_base_query()

    results = (
        query
        .with_entities(
            Report.category,
            Report.status,
            Report.portfolio,
            func.count(Report.id)
        )
        .group_by(Report.category, Report.status, Report.portfolio)
        .all()
    )

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 40
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, "Phola Park – Analytics Report")

    y -= 30
    pdf.setFont("Helvetica", 10)
    pdf.drawString(40, y, f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(40, y, "Category")
    pdf.drawString(160, y, "Status")
    pdf.drawString(260, y, "Portfolio")
    pdf.drawString(400, y, "Count")

    y -= 15
    pdf.setFont("Helvetica", 10)

    for category, status, portfolio, count in results:
        if y < 50:
            pdf.showPage()
            y = height - 40

        pdf.drawString(40, y, str(category))
        pdf.drawString(160, y, str(status))
        pdf.drawString(260, y, str(portfolio))
        pdf.drawString(400, y, str(count))
        y -= 15

    pdf.save()
    buffer.seek(0)

    return Response(
        buffer,
        mimetype="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=analytics_report.pdf"
        }
    )
