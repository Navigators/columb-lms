from django.shortcuts import render

def lms_index(request):
    return render(request, 'lms/index.html') 
def lms_addbook(request):
    return render(request, 'lms/addbook.html') 
def lms_addbook_new(request):
    if request.method == 'POST':
        if request.POST['funno'] == '01':
            return book_enter_base(request)
    else:
        return render(request, 'lms/addbook_new.html') 
def book_enter_base(request):
    try:
        #u = request.user
        isbn = request.POST[''] 
        name = request.POST['']
        input_code = request.POST['']+''
        author = request.POST['']
        type = request.POST['']
        publisher = Publisher.objects.get(name = request.POST[''])
        publish_date = request.POST['']
        price = request.POST['']
        keywords = request.POST['']+''
        series_name = request.POST['']+''
        edition_time = request.POST['']+''
        language = request.POST['']+''
        face_info = request.POST['']+''
        addons = request.POST['']+''
        cn = request.POST['']+''
        publish_periods = request.POST['']+''
        up_dept = request.POST['']+''
        content_intro = request.POST['']+''
        memo = request.POST['']+''
        total_count = 0
        loan_count = 0
        operater = 
        piclocation = request.POST['']+''
