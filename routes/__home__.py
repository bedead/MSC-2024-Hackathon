from flask import Blueprint, render_template, send_file

# Create a blueprint for the home routes
base_page_bp = Blueprint("landing_page", __name__)


# Define the route for the home page
@base_page_bp.route("/")
def home():
    return render_template("/base/landing_page.html")


@base_page_bp.route("/integration")
def integration():
    return render_template("/base/integration.html")


@base_page_bp.route("/contact")
def contact():
    return render_template("/base/contact.html")


@base_page_bp.route("/about")
def blog():
    return render_template("/base/blog_guide.html")


@base_page_bp.route("/about")
def about():
    return render_template("/base/about.html")


@base_page_bp.route("/blogs/time_management")
def blog_1():
    return render_template("/blogs/1.html")


@base_page_bp.route("/blogs/team_management")
def blog_2():
    return render_template("/blogs/2.html")


@base_page_bp.route("/blogs/task_management")
def blog_3():
    return render_template("/blogs/3.html")