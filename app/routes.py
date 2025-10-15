from flask import Blueprint, render_template, request, redirect, url_for, Response, flash
from .db import get_session
from .models import Search, Company, Lead, Contact, Job, OptOut
from services import cnae_map, seasonality, messaging
import csv
from io import StringIO

bp = Blueprint("core", __name__)

@bp.route("/")
def home():
    return render_template("home.html")

@bp.route("/buscar", methods=["POST"])
def buscar():
    seg = request.form.get("segmento","").strip() or "genérico"
    prod = request.form.get("produto","").strip() or "produto"
    uf = request.form.get("uf","BR").strip().upper() or "BR"

    session = get_session()
    search = Search(segmento=seg, produto=prod, uf=uf, status="queued")
    session.add(search); session.commit()

    # dispara a tarefa (com CELERY_TASK_ALWAYS_EAGER=1 roda inline)
    from tasks import run_prospecting
    run_prospecting.delay(search.id)

    flash("Busca iniciada! Os primeiros leads aparecerão em alguns instantes.", "success")
    return redirect(url_for("core.status", search_id=search.id))

@bp.route("/status/<int:search_id>")
def status(search_id):
    session = get_session()
    search = session.get(Search, search_id)
    jobs = (session.query(Job).filter_by(search_id=search_id)
            .order_by(Job.created_at.desc()).all())
    leads_count = session.query(Lead).filter_by(search_id=search_id).count()
    return render_template("status.html", search=search, jobs=jobs, leads_count=leads_count)

@bp.route("/resultado/<int:search_id>")
def resultado(search_id):
    session = get_session()
    search = session.get(Search, search_id)
    leads = (session.query(Lead).filter_by(search_id=search_id)
             .order_by(Lead.score.desc()).limit(100).all())

    textos = {l.id: messaging.gerar_texto_whatsapp(l, search.produto, search.segmento, l.janela_favoravel) for l in leads}

    cnaes, termos = cnae_map.mapear(search.segmento, search.produto)
    geo = search.uf if search.uf and search.uf != "BR" else "BR"
    saz = seasonality.sazonalidade_por_mes([search.produto] + termos, geo=geo)
    saz_pairs = [(int(r['mes']), float(r['indice'])) for r in saz.to_dict(orient='records')]

    return render_template("results.html", search=search, leads=leads, textos=textos, sazonalidade=saz_pairs)

@bp.route("/enriquecer_async/<int:search_id>")
def enriquecer_async(search_id):
    from tasks import run_enrichment
    run_enrichment.delay(search_id, top_n=25)
    flash("Enriquecimento iniciado para o Top 25. Volte em alguns instantes.", "success")
    return redirect(url_for("core.status", search_id=search_id))

@bp.route("/export_csv/<int:search_id>")
def export_csv(search_id):
    session = get_session()
    search = session.get(Search, search_id)
    leads = (session.query(Lead).filter_by(search_id=search_id)
             .order_by(Lead.score.desc()).all())

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(["Empresa","CNPJ","UF","Município","CNAE","Score","Prob_30d","Prob_90d","Janela_Favoravel","Site","Contatos","Enrichment_Status"])
    for l in leads:
        c = l.company
        contatos = "; ".join([f"{ct.tipo}:{ct.valor}" for ct in c.contacts[:3]]) if c.contacts else ""
        writer.writerow([
            c.nome_fantasia or c.razao_social,
            c.cnpj, c.uf, c.municipio, c.cnae_principal,
            l.score, l.prob_30d, l.prob_90d, l.janela_favoravel,
            c.site_url, contatos, l.enrichment_status
        ])
    output = si.getvalue()
    return Response(output, mimetype="text/csv",
                    headers={"Content-Disposition": f"attachment; filename=leads_search_{search_id}.csv"})

@bp.route("/optout", methods=["GET","POST"])
def optout():
    session = get_session()
    if request.method == "POST":
        company = request.form.get("company","").strip()
        email = request.form.get("email","").strip()
        reason = request.form.get("reason","").strip()
        if company and email:
            session.add(OptOut(company_name=company, email=email, reason=reason))
            session.commit()
            flash("Solicitação registrada. Processaremos a remoção.", "success")
            return redirect(url_for("core.optout"))
        else:
            flash("Informe ao menos empresa e e-mail.", "info")
    return render_template("optout.html")
