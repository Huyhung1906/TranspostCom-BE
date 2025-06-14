from google.genai import Client
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from utils.prompt import *
# Đặt API key từ Google GenAI
api_key = "AIzaSyDIWoW6Wn049vv6i_Qr0G5eTEqc1Hd7aLg"  # Thay thế với API key từ Google


# Tạo một client cho Google GenAI
client = Client(api_key=api_key)

def generate_sql(question):
    try:
        prompt = prompt_sql.format(question=question)
        # Gửi yêu cầu tới Google GenAI để sinh câu lệnh SQL từ câu hỏi
        response = client.models.generate_content(
            model="gemini-2.0-flash",  # Chọn mô hình bạn muốn sử dụng (ví dụ: gemini-2.0-flash)
            contents=prompt
        )
        # Trả về câu lệnh SQL sinh được
        sql = response.text.strip()
        sql = sql.replace('```sql', '').replace('```', '').strip()
        return sql
    except Exception as e:
        return str(e)
def execute_sql(sql):
    try:
        # Mở kết nối đến cơ sở dữ liệu
        with connection.cursor() as cursor:
            cursor.execute(sql)  # Thực thi câu lệnh SQL
            # Lấy kết quả trả về dưới dạng list of tuples
            result = cursor.fetchall()
            # Lấy tên cột
            columns = [col[0] for col in cursor.description]
            # Trả về kết quả dưới dạng danh sách các từ điển (key: tên cột, value: giá trị)
            result_dict = [dict(zip(columns, row)) for row in result]
        return result_dict
    except Exception as e:
        return str(e)
@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question = data.get("question", "")
        try:
            # Sinh câu lệnh SQL từ câu hỏi
            sql = generate_sql(question)
            if sql.startswith("SELECT"):
                # Thực thi câu lệnh SQL nếu là SELECT
                result = execute_sql(sql)
                answer = generate_answer_from_result(question, sql, result)
                return JsonResponse({
                    "sql": sql,
                    "result": result,
                    "answer": answer
                })
            else:
                return JsonResponse({"text": "Mình là một AI chỉ có thể hiển thị tìm kiếm các thông tin cho bạn, các hành động gây ảnh hưởng đến dữ liệu mình không làm được .","answer": sql}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e),"sql": sql}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
def generate_answer_from_result(question, sql, result):
    try:
        formatted_prompt = prompt_answer.format(
            question=question,
            sql=sql,
            result=result
        )
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=formatted_prompt  # dùng nội dung đã được format
        )
        return response.text.strip()
    except Exception as e:
        return f"Không thể tạo câu trả lời ngôn ngữ tự nhiên: {str(e)}"