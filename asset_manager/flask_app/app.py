import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "asset_manager_flask_secret_key_change_me_in_production"

# FastAPI Backend URL
API_URL = os.getenv("API_URL", "http://127.0.0.1:8001/api")


def get_categories():
    try:
        response = requests.get(f"{API_URL}/categories")
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        pass
    return []


@app.route("/")
def dashboard():
    stats = {}
    recent_assets = []
    error_msg = None
    try:
        stats_resp = requests.get(f"{API_URL}/stats")
        if stats_resp.status_code == 200:
            stats = stats_resp.json()

        assets_resp = requests.get(f"{API_URL}/assets?limit=5")
        if assets_resp.status_code == 200:
            recent_assets = assets_resp.json()
    except requests.RequestException:
        error_msg = "Could not connect to the API backend. Please ensure the FastAPI service is running."

    return render_template(
        "dashboard.html", stats=stats, recent_assets=recent_assets, error_msg=error_msg
    )


@app.route("/assets")
def list_assets():
    search = request.args.get("search", "")
    status = request.args.get("status", "")
    category_id = request.args.get("category_id", "")

    categories = get_categories()

    params = {}
    if search:
        params["search"] = search
    if status:
        params["status"] = status
    if category_id:
        params["category_id"] = category_id

    assets = []
    error_msg = None
    try:
        response = requests.get(f"{API_URL}/assets", params=params)
        if response.status_code == 200:
            assets = response.json()
    except requests.RequestException:
        error_msg = "Could not fetch assets from backend."

    return render_template(
        "assets.html",
        assets=assets,
        categories=categories,
        search=search,
        status=status,
        category_id=category_id,
        error_msg=error_msg,
    )


@app.route("/assets/<int:asset_id>")
def asset_detail(asset_id):
    try:
        response = requests.get(f"{API_URL}/assets/{asset_id}")
        if response.status_code == 200:
            asset = response.json()
            return render_template("asset_detail.html", asset=asset)
        else:
            flash(
                f"Asset not found: {response.json().get('detail', 'Unknown error')}",
                "danger",
            )
    except requests.RequestException:
        flash("Could not connect to backend to retrieve asset details.", "danger")
    return redirect(url_for("list_assets"))


@app.route("/assets/add", methods=["GET", "POST"])
def add_asset():
    categories = get_categories()
    if request.method == "POST":
        payload = {
            "name": request.form["name"],
            "serial_number": request.form["serial_number"],
            "category_id": int(request.form["category_id"]),
            "status": "AVAILABLE",
            "purchase_date": request.form["purchase_date"],
            "price": float(request.form["price"]),
            "description": request.form["description"],
        }
        try:
            response = requests.post(f"{API_URL}/assets", json=payload)
            if response.status_code == 201:
                flash("Asset successfully created!", "success")
                return redirect(url_for("list_assets"))
            else:
                flash(
                    f"Failed to create asset: {response.json().get('detail', 'Error')}",
                    "danger",
                )
        except requests.RequestException:
            flash("Could not connect to backend to save asset.", "danger")

    return render_template("add_asset.html", categories=categories)


@app.route("/assets/<int:asset_id>/checkout", methods=["GET", "POST"])
def checkout_asset(asset_id):
    asset = None
    try:
        response = requests.get(f"{API_URL}/assets/{asset_id}")
        if response.status_code == 200:
            asset = response.json()
        else:
            flash("Asset not found.", "danger")
            return redirect(url_for("list_assets"))
    except requests.RequestException:
        flash("Could not connect to backend.", "danger")
        return redirect(url_for("list_assets"))

    if request.method == "POST":
        payload = {
            "employee_name": request.form["employee_name"],
            "employee_email": request.form["employee_email"],
            "expected_return_date": request.form["expected_return_date"],
            "notes": request.form["notes"],
        }
        try:
            response = requests.post(
                f"{API_URL}/assets/{asset_id}/checkout", json=payload
            )
            if response.status_code == 200:
                flash(f"Asset '{asset['name']}' checked out successfully!", "success")
                return redirect(url_for("asset_detail", asset_id=asset_id))
            else:
                flash(
                    f"Checkout failed: {response.json().get('detail', 'Error')}",
                    "danger",
                )
        except requests.RequestException:
            flash("Could not connect to backend to process checkout.", "danger")

    return render_template("checkout.html", asset=asset)


@app.route("/assets/<int:asset_id>/return", methods=["POST"])
def return_asset(asset_id):
    notes = request.form.get("notes", "")
    try:
        response = requests.post(
            f"{API_URL}/assets/{asset_id}/return", json={"notes": notes}
        )
        if response.status_code == 200:
            flash("Asset returned successfully!", "success")
        else:
            flash(
                f"Failed to return asset: {response.json().get('detail', 'Error')}",
                "danger",
            )
    except requests.RequestException:
        flash("Could not connect to backend to process return.", "danger")

    return redirect(url_for("asset_detail", asset_id=asset_id))


@app.route("/assets/<int:asset_id>/maintenance", methods=["GET", "POST"])
def start_maintenance(asset_id):
    asset = None
    try:
        response = requests.get(f"{API_URL}/assets/{asset_id}")
        if response.status_code == 200:
            asset = response.json()
        else:
            flash("Asset not found.", "danger")
            return redirect(url_for("list_assets"))
    except requests.RequestException:
        flash("Could not connect to backend.", "danger")
        return redirect(url_for("list_assets"))

    if request.method == "POST":
        payload = {
            "description": request.form["description"],
            "cost": float(request.form["cost"] or 0),
            "start_date": request.form["start_date"],
        }
        try:
            response = requests.post(
                f"{API_URL}/assets/{asset_id}/maintenance/start", json=payload
            )
            if response.status_code == 200:
                flash("Maintenance log started!", "success")
                return redirect(url_for("asset_detail", asset_id=asset_id))
            else:
                flash(
                    f"Failed to start maintenance: {response.json().get('detail', 'Error')}",
                    "danger",
                )
        except requests.RequestException:
            flash("Could not connect to backend to register maintenance.", "danger")

    return render_template("maintenance.html", asset=asset)


@app.route("/assets/<int:asset_id>/maintenance/end", methods=["POST"])
def end_maintenance(asset_id):
    cost = request.form.get("cost")
    payload = {}
    if cost:
        payload["cost"] = float(cost)
    try:
        response = requests.post(
            f"{API_URL}/assets/{asset_id}/maintenance/end", json=payload
        )
        if response.status_code == 200:
            flash("Maintenance completed. Asset is now available!", "success")
        else:
            flash(
                f"Failed to end maintenance: {response.json().get('detail', 'Error')}",
                "danger",
            )
    except requests.RequestException:
        flash("Could not connect to backend to complete maintenance.", "danger")

    return redirect(url_for("asset_detail", asset_id=asset_id))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)
