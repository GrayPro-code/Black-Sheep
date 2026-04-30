import os
from flask import render_template, request, redirect, url_for, current_app, flash
from werkzeug.utils import secure_filename
from models import db, PortfolioCard, slugify
from . import admin_bp
from .forms import PortfolioForm


def save_image(file):
    if not file or not file.filename:
        return None

    filename = secure_filename(file.filename)
    upload_folder = os.path.join(current_app.root_path, "static/uploads")
    os.makedirs(upload_folder, exist_ok=True)
    
    path = os.path.join(upload_folder, filename)
    file.save(path)

    return f"/static/uploads/{filename}"


@admin_bp.route("/", methods=["GET", "POST"])
def admin_index():
    form = PortfolioForm()

    if form.validate_on_submit():
        image_path = save_image(form.image.data)

        card = PortfolioCard(
            title=form.title.data,
            slug=slugify(form.title.data),                 
            category=form.category.data,
            category_slug=slugify(form.category.data),     
            year=form.year.data,
            tech1=form.tech1.data,
            tech2=form.tech2.data,
            image=image_path
        )

        try:
            db.session.add(card)
            db.session.commit()
            flash("Карточка добавлена!", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"DB error: {e}")
            flash("Ошибка при сохранении", "danger")

        return redirect(url_for("admin.admin_index"))

    cards = PortfolioCard.query.all()
    return render_template("admin.html", form=form, cards=cards)


@admin_bp.route("/edit/<int:card_id>", methods=["GET", "POST"])
def edit_card(card_id):
    card = PortfolioCard.query.get_or_404(card_id)
    form = PortfolioForm(obj=card)

    if form.validate_on_submit():
        card.title = form.title.data
        card.slug = slugify(card.title)                     

        card.category = form.category.data
        card.category_slug = slugify(card.category)      

        card.year = form.year.data
        card.tech1 = form.tech1.data
        card.tech2 = form.tech2.data

        if form.image.data:
            card.image = save_image(form.image.data)

        db.session.commit()
        flash("Карточка обновлена", "success")
        return redirect(url_for("admin.admin_index"))

    return render_template("edit.html", form=form, card=card)



@admin_bp.route("/delete/<int:card_id>", methods=["POST"])
def delete_card(card_id):
    card = PortfolioCard.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()
    flash("Карточка удалена", "success")
    return redirect(url_for("admin.admin_index"))
