from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponseRedirect
from .models import Ticket
from django.contrib.auth.decorators import login_required

def answer_question(request, ticket_id):
    if request.method == 'POST':
        ticket = Ticket.objects.get(pk=ticket_id)
        if ticket.progressingDay == 1:
            day1_question = ticket.day1_question
            day1_question.answer = request.POST.get('answer')
            day1_question.save()
        else:
            after_day1_question = ticket.after_day1_question
            after_day1_question.answer = request.POST.get('answer')
            after_day1_question.save()
        return HttpResponseRedirect('/thank-you/')
    else:
        return render(request, 'answer_form.html') 

@login_required
def ticket_detail(request, ticket_number):
    ticket = get_object_or_404(Ticket, ticketNumber=ticket_number)
    if not request.user.tickets.filter(ticketNumber=ticket_number).exists():
        return redirect('permission_denied')
    context = {
        'ticket': ticket,
    }
    return render(request, 'ticket_detail.html', context)
