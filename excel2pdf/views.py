import openpyxl
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import UploadFileForm

def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        wb = openpyxl.load_workbook(file)
        sheet = wb.active

        products = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            values = list(row[:4]) + [""] * (4 - len(row[:4]))
            name, variant, mrp, price = values

            if not any([name, variant, mrp, price]):
                continue

            # Convert numeric floats to int if whole number
            if isinstance(mrp, float) and mrp.is_integer():
                mrp = int(mrp)
            if isinstance(price, float) and price.is_integer():
                price = int(price)

            products.append({
                "name": name,
                "variant": variant,
                "mrp": mrp,
                "price": price
            })

        request.session['products'] = products
        return redirect('preview_file')

    form = UploadFileForm()
    return render(request, "upload.html", {"form": form})



def preview_file(request):
    products = request.session.get('products', [])
    if not products:
        return redirect('upload_file')
    return render(request, "preview.html", {"products": products})


def download_pdf(request):
    products = request.session.get('products', [])
    if not products:
        return redirect('upload_file')

    template = get_template("pdf_template.html")
    html = template.render({"products": products})

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="products.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)
    return response


def view_pdf(request):
    products = request.session.get('products', [])
    if not products:
        return redirect('upload_file')

    template = get_template("pdf_template.html")
    html = template.render({"products": products})

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="products.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)
    return response
