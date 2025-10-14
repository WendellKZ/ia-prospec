from flask import Blueprint, render_template, request, redirect, url_for, Response, flash
from .db import get_session, init_db
from .models import Search, Company, Lead, Contact, Job, OptOut

bp = Blueprint("core", __name__)

@bp.route("/")
def home():
    return "<h3>IA Prospec online ✅</h3><p>Use /status/1 e /resultado/1 após rodar uma busca.</p>"
