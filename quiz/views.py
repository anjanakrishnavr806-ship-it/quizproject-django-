from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Question, Choice, Result


# ---------------- LOGIN VIEW ----------------
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('quiz')
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})


# ---------------- REGISTER VIEW ----------------
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz')
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})


# ---------------- QUIZ VIEW ----------------
@login_required
def quiz_view(request):
    questions = Question.objects.all()

    if request.method == "POST":
        score = 0
        results = []

        for question in questions:
            selected_choice_id = request.POST.get(f"question_{question.id}")
            selected_choice = None
            correct_choice = question.choice_set.filter(is_correct=True).first()

            if selected_choice_id:
                selected_choice = Choice.objects.get(id=selected_choice_id)

                if selected_choice.is_correct:
                    score += 1

            results.append({
                "question": question,
                "selected": selected_choice,
                "correct": correct_choice
            })

        Result.objects.create(user=request.user, score=score)

        return render(request, "quiz/result.html", {
            "score": score,
            "results": results,
            "total": questions.count()
        })

    return render(request, "quiz/quiz.html", {"questions": questions})

# ---------------- RESULTS HISTORY ----------------
@login_required
def results_history_view(request):
    results = Result.objects.filter(user=request.user).order_by('-id')
    return render(request, "quiz/results_history.html", {"results": results})


# ---------------- LOGOUT VIEW ----------------
def logout_view(request):
    logout(request)
    return redirect('login')