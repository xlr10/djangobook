import logging

from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect

from ..models import Question
from ..models import Answer

logger = logging.getLogger('pybo')

def category_index(request, category):
    logger.info("INFO 레벨로 출력")
    """
    pybo 카테고리 분기
    """

    if category == 'qna':
        return redirect('pybo:index')

    
    return redirect('pybo:index')



def index(request):
    logger.info("INFO 레벨로 출력")
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so, 'category':'qna'}  # <------ so 추가
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """

    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    question = get_object_or_404(Question, pk=question_id)
    #answer_list = question.answer_set.all().annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')

    # 정렬
    if so == 'recommend':
        answer_list = question.answer_set.all().annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        answer_list = question.answer_set.all().annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        answer_list = question.answer_set.all().order_by('-create_date')

    
    
    # 페이징처리
    #모든 질문 다옴
    #질문 아이디에 따른 질문만
    paginator = Paginator(answer_list, 3)  # 페이지당 3개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question': question, 'answer_list':page_obj , 'page': page, 'kw': kw, 'so': so}
    return render(request, 'pybo/question_detail.html', context)
