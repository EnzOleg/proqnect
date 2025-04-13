from django.shortcuts import render
from .openai_service import ask_gpt, ask_gpt_in_help
from django.http import JsonResponse

# Create your views here.
def gpt_assist(request):
    prompt = request.GET.get("prompt", "")
    if not prompt:
        return JsonResponse({"error": "No prompt provided"}, status=400)
    answer = ask_gpt(prompt)
    return JsonResponse({"response": answer})


def gpt_chat_assistent(request):
    prompt = request.GET.get("prompt", "")
    if not prompt:
        return JsonResponse({"error": "No prompt provided"}, status=400)
    answer = ask_gpt_in_help(prompt)
    return JsonResponse({"response": answer})