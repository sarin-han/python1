import tkinter as tk
from tkcalendar import DateEntry
import os
import json
from tkinter import ttk, messagebox
from datetime import datetime

def format_date_with_weekday(date_str):
    """날짜 문자열에 요일을 추가하는 함수"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        weekdays = ['월', '화', '수', '목', '금', '토', '일']
        weekday = weekdays[date_obj.weekday()]
        return f"{date_str} ({weekday})"
    except:
        return date_str
    
def save_record(date, amount, category):
    """가계부 기록을 저장하는 함수"""
    try:
        if not amount.isdigit():
            messagebox.showerror("⚠️ 입력 오류", "금액은 숫자만 입력해주세요! 😊")
            return False
            
        if not category:
            messagebox.showerror("⚠️ 입력 오류", "카테고리를 선택해주세요! 🏷️")
            return False
            
        data = {"날짜": date, "금액": amount, "카테고리": category, "등록시간": datetime.now().strftime("%Y-%m-%d %H:%M")}

        if os.path.exists("data.json"):
            with open("data.json", "r", encoding="utf-8") as file:
                loaded_data = json.load(file)
                loaded_data.append(data)
        else:
            loaded_data = [data]

        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(loaded_data, file, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("✅ 저장 완료", "기록이 성공적으로 저장되었어요! 🎉")
        return True
        
    except Exception as e:
        messagebox.showerror("❌ 오류", f"저장 중 오류가 발생했어요: {e}")
        return False

def update_record(index, date, amount, category):
    """기록을 수정하는 함수"""
    try:
        if not amount.isdigit():
            messagebox.showerror("⚠️ 입력 오류", "금액은 숫자만 입력해주세요! 😊")
            return False
            
        if not category:
            messagebox.showerror("⚠️ 입력 오류", "카테고리를 선택해주세요! 🏷️")
            return False
            
        if os.path.exists("data.json"):
            with open("data.json", "r", encoding="utf-8") as file:
                loaded_data = json.load(file)
            
            if 0 <= index < len(loaded_data):
                loaded_data[index]["날짜"] = date
                loaded_data[index]["금액"] = amount
                loaded_data[index]["카테고리"] = category
                loaded_data[index]["수정시간"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                with open("data.json", "w", encoding="utf-8") as file:
                    json.dump(loaded_data, file, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("✅ 수정 완료", "기록이 성공적으로 수정되었어요! 🎉")
                return True
            else:
                messagebox.showerror("❌ 오류", "잘못된 기록입니다.")
                return False
        else:
            messagebox.showerror("❌ 오류", "기록 파일을 찾을 수 없어요.")
            return False
        
    except Exception as e:
        messagebox.showerror("❌ 오류", f"수정 중 오류가 발생했어요: {e}")
        return False

def delete_record(index):
    """기록을 삭제하는 함수"""
    try:
        if os.path.exists("data.json"):
            with open("data.json", "r", encoding="utf-8") as file:
                loaded_data = json.load(file)
            
            if 0 <= index < len(loaded_data):
                deleted_record = loaded_data.pop(index)
                
                with open("data.json", "w", encoding="utf-8") as file:
                    json.dump(loaded_data, file, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("✅ 삭제 완료", f"기록이 성공적으로 삭제되었어요! 🗑️\n({deleted_record['날짜']} - {deleted_record['카테고리']} - {int(deleted_record['금액']):,}원)")
                return True
            else:
                messagebox.showerror("❌ 오류", "잘못된 기록입니다.")
                return False
        else:
            messagebox.showerror("❌ 오류", "기록 파일을 찾을 수 없어요.")
            return False
        
    except Exception as e:
        messagebox.showerror("❌ 오류", f"삭제 중 오류가 발생했어요: {e}")
        return False

def save_goals(goals_data):
    """목표 데이터를 저장하는 함수"""
    try:
        current_month = datetime.now().strftime("%Y-%m")
        
        # 기존 goals.json 로드
        if os.path.exists("goals.json"):
            with open("goals.json", "r", encoding="utf-8") as file:
                all_goals = json.load(file)
        else:
            all_goals = []
        
        # 현재 월의 기존 목표들 제거
        all_goals = [goal for goal in all_goals if goal.get("월") != current_month]
        
        # 새로운 목표들 추가
        for category, amount in goals_data.items():
            if amount and amount.isdigit():
                goal_data = {
                    "카테고리": category,
                    "목표금액": int(amount),
                    "월": current_month,
                    "설정시간": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                all_goals.append(goal_data)
        
        with open("goals.json", "w", encoding="utf-8") as file:
            json.dump(all_goals, file, ensure_ascii=False, indent=2)
        
        return True
        
    except Exception as e:
        messagebox.showerror("❌ 오류", f"목표 저장 중 오류가 발생했어요: {e}")
        return False

def get_current_month_goals():
    """현재 월의 목표들을 가져오는 함수"""
    try:
        current_month = datetime.now().strftime("%Y-%m")
        if os.path.exists("goals.json"):
            with open("goals.json", "r", encoding="utf-8") as file:
                all_goals = json.load(file)
            return {goal["카테고리"]: goal["목표금액"] for goal in all_goals if goal.get("월") == current_month}
        return {}
    except:
        return {}

def calculate_monthly_spending(category=None):
    """현재 월의 지출을 계산하는 함수"""
    try:
        current_month = datetime.now().strftime("%Y-%m")
        if not os.path.exists("data.json"):
            return 0
            
        with open("data.json", "r", encoding="utf-8") as file:
            records = json.load(file)
        
        total = 0
        for record in records:
            record_month = record["날짜"][:7]
            if record_month == current_month:
                if category is None or record["카테고리"] == category:
                    total += int(record["금액"])
        
        return total
    except:
        return 0

def show_goal_setting():
    """목표 설정 창을 보여주는 함수"""
    goal_window = tk.Toplevel()
    goal_window.title("🎯 이번 달 목표 설정")
    goal_window.geometry("500x850")
    goal_window.configure(bg="#fff9c4")
    goal_window.grab_set()
    
    # 제목
    tk.Label(
        goal_window,
        text="🎯 이번 달 지출 목표 설정",
        font=("맑은 고딕", 20, "bold"),
        fg="#e17055",
        bg="#fff9c4"
    ).pack(pady=30)
    
    # 현재 월 표시
    current_month_text = datetime.now().strftime("%Y년 %m월")
    tk.Label(
        goal_window,
        text=f"📅 {current_month_text}",
        font=("맑은 고딕", 14),
        fg="#636e72",
        bg="#fff9c4"
    ).pack(pady=(0, 20))
    
    # 입력 프레임
    input_frame = tk.Frame(goal_window, bg="#fffef7", relief="solid", borderwidth=2)
    input_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
    
    tk.Label(
        input_frame,
        text="💰 카테고리별 목표 금액을 입력하세요",
        font=("맑은 고딕", 14, "bold"),
        fg="#2d3436",
        bg="#fffef7"
    ).pack(pady=20)
    
    # 기존 목표 불러오기
    existing_goals = get_current_month_goals()
    
    categories = ["전체", "식비", "쇼핑", "교통비", "취미", "선물", "자기개발", "동아리", "기타"]
    entries = {}
    
    # 카테고리별 입력 필드 (2열로 배치)
    for i, category in enumerate(categories):
        row_frame = tk.Frame(input_frame, bg="#fffef7")
        row_frame.pack(fill="x", padx=30, pady=8)
        
        # 현재 지출 계산
        if category == "전체":
            current_spending = calculate_monthly_spending()
        else:
            current_spending = calculate_monthly_spending(category)
        
        # 카테고리 라벨
        cat_label = tk.Label(
            row_frame,
            text=f"🏷️ {category}",
            font=("맑은 고딕", 12, "bold"),
            bg="#fffef7",
            fg="#2d3436",
            width=8,
            anchor="w"
        )
        cat_label.pack(side="left", padx=(0, 10))
        
        # 현재 지출 표시
        spending_label = tk.Label(
            row_frame,
            text=f"현재: {current_spending:,}원",
            font=("맑은 고딕", 9),
            bg="#fffef7",
            fg="#636e72",
            width=12,
            anchor="w"
        )
        spending_label.pack(side="left", padx=(0, 10))
        
        # 목표 입력
        tk.Label(
            row_frame,
            text="목표:",
            font=("맑은 고딕", 10),
            bg="#fffef7",
            fg="#2d3436"
        ).pack(side="left", padx=(0, 5))
        
        entry = tk.Entry(
            row_frame,
            font=("맑은 고딕", 11),
            width=12,
            justify="right",
            bg="white",
            relief="solid",
            borderwidth=1
        )
        
        # 기존 목표가 있으면 표시
        if category in existing_goals:
            entry.insert(0, str(existing_goals[category]))
            
        entry.pack(side="left", padx=(0, 5))
        entries[category] = entry
        
        tk.Label(
            row_frame,
            text="원",
            font=("맑은 고딕", 10),
            bg="#fffef7",
            fg="#2d3436"
        ).pack(side="left")
    
    # 버튼 프레임
    button_frame = tk.Frame(goal_window, bg="#fff9c4")
    button_frame.pack(fill="x", padx=30, pady=(0, 30))
    
    def save_all_goals():
        goals_data = {}
        for category, entry in entries.items():
            amount = entry.get().strip()
            if amount:
                goals_data[category] = amount
        
        if save_goals(goals_data):
            messagebox.showinfo("✅ 저장 완료", "목표가 성공적으로 설정되었어요! 🎉")
            goal_window.destroy()
    
    # 저장 버튼
    save_btn = tk.Button(
        button_frame,
        text="💾 목표 저장하기",
        command=save_all_goals,
        bg="#00b894",
        fg="white",
        font=("맑은 고딕", 14, "bold"),
        relief="solid",
        borderwidth=2,
        padx=40,
        pady=12,
        cursor="hand2"
    )
    save_btn.pack()

def edit_record_window(index, record):
    """기록 수정 창을 여는 함수"""
    edit_window = tk.Toplevel()
    edit_window.title(f"✏️ 기록 수정하기")
    edit_window.geometry("400x500")
    edit_window.configure(bg="#fff9c4")
    edit_window.grab_set()
    
    tk.Label(
        edit_window,
        text="✏️ 기록 수정하기",
        font=("맑은 고딕", 18, "bold"),
        fg="#e17055",
        bg="#fff9c4"
    ).pack(pady=20)
    
    input_frame = tk.Frame(edit_window, bg="#fffef7", relief="solid", borderwidth=2)
    input_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    # 날짜 입력
    date_frame = tk.Frame(input_frame, bg="#fff9c4", relief="solid", borderwidth=1)
    date_frame.pack(fill="x", padx=20, pady=20)
    
    tk.Label(date_frame, text="📅 날짜", font=("맑은 고딕", 12, "bold"), bg="#fff9c4", fg="#2d3436").pack(anchor="w", padx=15, pady=(10, 5))
    
    edit_date_entry = DateEntry(
        date_frame, width=12, background='#fdcb6e', foreground='#2d3436',
        borderwidth=2, date_pattern='yyyy-mm-dd', font=("맑은 고딕", 11)
    )
    try:
        edit_date_entry.set_date(datetime.strptime(record['날짜'], '%Y-%m-%d').date())
    except:
        pass
    edit_date_entry.pack(fill="x", padx=15, pady=(0, 10))
    
    # 카테고리 입력
    category_frame = tk.Frame(input_frame, bg="#fff9c4", relief="solid", borderwidth=1)
    category_frame.pack(fill="x", padx=20, pady=(0, 20))
    
    tk.Label(category_frame, text="🏷️ 카테고리", font=("맑은 고딕", 12, "bold"), bg="#fff9c4", fg="#2d3436").pack(anchor="w", padx=15, pady=(10, 5))
    
    edit_category_combo = ttk.Combobox(
        category_frame, values=["식비", "쇼핑", "교통비", "취미", "선물", "자기개발", "동아리", "기타"],
        state="readonly", font=("맑은 고딕", 11)
    )
    edit_category_combo.set(record.get('카테고리', ''))
    edit_category_combo.pack(fill="x", padx=15, pady=(0, 10))
    
    # 금액 입력
    price_frame = tk.Frame(input_frame, bg="#fff9c4", relief="solid", borderwidth=1)
    price_frame.pack(fill="x", padx=20, pady=(0, 20))
    
    tk.Label(price_frame, text="💰 금액 (원)", font=("맑은 고딕", 12, "bold"), bg="#fff9c4", fg="#2d3436").pack(anchor="w", padx=15, pady=(10, 5))
    
    edit_amount_entry = tk.Entry(price_frame, font=("맑은 고딕", 14), relief="solid", borderwidth=1, justify="right", bg="#fffef7")
    edit_amount_entry.insert(0, record.get('금액', ''))
    edit_amount_entry.pack(fill="x", padx=15, pady=(0, 10))
    
    # 버튼 프레임
    button_frame = tk.Frame(input_frame, bg="#fffef7")
    button_frame.pack(fill="x", padx=20, pady=20)
    
    def save_changes():
        date = edit_date_entry.get()
        amount = edit_amount_entry.get().strip()
        category = edit_category_combo.get()
        
        if update_record(index, date, amount, category):
            edit_window.destroy()
            if hasattr(edit_window, 'parent_refresh'):
                edit_window.parent_refresh()
    
    save_btn = tk.Button(button_frame, text="💾 저장하기", command=save_changes, bg="#00b894", fg="white",
                        font=("맑은 고딕", 12, "bold"), relief="solid", borderwidth=2, padx=30, pady=8, cursor="hand2")
    save_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
    
    cancel_btn = tk.Button(button_frame, text="❌ 취소", command=edit_window.destroy, bg="#ddd", fg="#2d3436",
                          font=("맑은 고딕", 12, "bold"), relief="solid", borderwidth=2, padx=30, pady=8, cursor="hand2")
    cancel_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
    
    edit_amount_entry.bind('<Return>', lambda e: save_changes())
    
    return edit_window

def show_records():
    """저장된 기록을 보여주는 함수"""
    new_window = tk.Toplevel(root)
    new_window.title("🌻 내 가계부 내역")
    new_window.geometry("900x700")
    new_window.configure(bg="#fff9c4")
    
    # 상단 요약 패널
    summary_panel = tk.Frame(new_window, bg="#ffeaa7", relief="solid", borderwidth=2)
    summary_panel.pack(fill="x", padx=20, pady=20)
    
    tk.Label(summary_panel, text="🌻 내 가계부 요약", font=("맑은 고딕", 20, "bold"), fg="#2d3436", bg="#ffeaa7").pack(pady=(15, 10))
    
    summary_frame = tk.Frame(summary_panel, bg="#ffeaa7")
    summary_frame.pack(fill="x", padx=20, pady=(0, 15))
    
    # 필터 프레임
    filter_frame = tk.Frame(new_window, bg="#fff9c4")
    filter_frame.pack(fill="x", padx=20, pady=10)
    
    tk.Label(filter_frame, text="🔍 카테고리:", font=("맑은 고딕", 12, "bold"), bg="#fff9c4", fg="#2d3436").pack(side="left", padx=(0, 10))
    
    filter_combo = ttk.Combobox(filter_frame, values=["전체", "식비", "쇼핑", "교통비", "취미", "선물", "자기개발", "동아리", "기타"],
                               state="readonly", width=15, font=("맑은 고딕", 11))
    filter_combo.pack(side="left", padx=(0, 10))
    filter_combo.set("전체")
    
    # 상세 기록 프레임
    detail_frame = tk.Frame(new_window, bg="#fff9c4")
    detail_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
    
    tk.Label(detail_frame, text="📝 상세 기록", font=("맑은 고딕", 14, "bold"), bg="#fff9c4", fg="#2d3436").pack(anchor="w", pady=(0, 10))
    
    # 스크롤 가능한 프레임
    canvas = tk.Canvas(detail_frame, bg="#fffef7")
    scrollbar = ttk.Scrollbar(detail_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#fffef7")
    
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def load_and_display_records():
        # 기존 내용 지우기
        for widget in summary_frame.winfo_children():
            widget.destroy()
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        
        if not os.path.exists("data.json"):
            tk.Label(summary_frame, text="💡 아직 기록이 없어요!\n메인 화면에서 첫 기록을 추가해보세요 🌟",
                    font=("맑은 고딕", 14), fg="#636e72", bg="#ffeaa7", justify="center").pack(pady=20)
            tk.Label(scrollable_frame, text="🌻 새로운 가계부를 시작해보세요!", font=("맑은 고딕", 16),
                    bg="#fffef7", fg="#636e72").pack(pady=50)
            return
            
        try:
            with open("data.json", "r", encoding="utf-8") as file:
                loaded_data = json.load(file)
                
            if not loaded_data:
                tk.Label(summary_frame, text="💡 저장된 기록이 없어요!", font=("맑은 고딕", 14), fg="#636e72", bg="#ffeaa7").pack(pady=20)
                tk.Label(scrollable_frame, text="🌻 첫 기록을 추가해보세요!", font=("맑은 고딕", 16), bg="#fffef7", fg="#636e72").pack(pady=50)
                return
                
            selected_filter = filter_combo.get()
            current_month = datetime.now().strftime("%Y-%m")
            
            # 현재 월 데이터만 필터링
            current_month_data = [record for record in loaded_data if record["날짜"][:7] == current_month]
            
            # 선택된 카테고리로 필터링
            if selected_filter == "전체":
                filtered_records = current_month_data
                total_amount = sum(int(record.get('금액', 0)) for record in current_month_data)
            else:
                filtered_records = [record for record in current_month_data if record.get('카테고리') == selected_filter]
                total_amount = sum(int(record.get('금액', 0)) for record in filtered_records)
            
            # 목표 데이터 가져오기
            goals = get_current_month_goals()
            
            # 요약 정보 표시
            summary_top = tk.Frame(summary_frame, bg="#ffeaa7")
            summary_top.pack(fill="x", pady=(0, 15))
            
            # 지출 정보 박스
            spend_info = tk.Frame(summary_top, bg="#fd79a8", relief="solid", borderwidth=2)
            spend_info.pack(side="left", fill="both", expand=True, padx=(0, 10))
            
            if selected_filter == "전체":
                spend_title = "💰 이번 달 총 지출"
            else:
                spend_title = f"🏷️ {selected_filter} 지출"
            
            tk.Label(spend_info, text=spend_title, font=("맑은 고딕", 12, "bold"), bg="#fd79a8", fg="#2d3436").pack(pady=(10, 5))
            tk.Label(spend_info, text=f"{total_amount:,}원", font=("맑은 고딕", 18, "bold"), bg="#fd79a8", fg="#d63031").pack(pady=(0, 10))
            
            # 목표 대비 정보 박스 (목표가 있을 때만)
            if selected_filter in goals:
                goal_amount = goals[selected_filter]
                remaining = goal_amount - total_amount
                progress_rate = (total_amount / goal_amount) * 100 if goal_amount > 0 else 0
                
                # 진행률에 따른 색상 결정
                if progress_rate <= 70:
                    goal_color = "#ffffff"
                    status_text = "👍 Good!"
                elif progress_rate <= 90:
                    goal_color = "#f9f8f8"
                    status_text = "⚠️ 주의"
                else:
                    goal_color = "#ffffff"
                    status_text = "🚨 위험"
                
                goal_info = tk.Frame(summary_top, bg="#a29bfe", relief="solid", borderwidth=2)
                goal_info.pack(side="left", fill="both", expand=True, padx=5)
                
                tk.Label(goal_info, text=f"🎯 목표 ({goal_amount:,}원)", font=("맑은 고딕", 12, "bold"), bg="#a29bfe", fg="#2d3436").pack(pady=(10, 5))
                
                if remaining >= 0:
                    tk.Label(goal_info, text=f"남은 금액", font=("맑은 고딕", 10), bg="#a29bfe", fg="#ffffff").pack()
                    tk.Label(goal_info, text=f"{remaining:,}원", font=("맑은 고딕", 16, "bold"), bg="#a29bfe", fg="#000000").pack()
                else:
                    tk.Label(goal_info, text=f"초과 금액", font=("맑은 고딕", 10), bg="#a29bfe", fg="#ffffff").pack()
                    tk.Label(goal_info, text=f"{abs(remaining):,}원", font=("맑은 고딕", 16, "bold"), bg="#a29bfe", fg="#e17055").pack()
                
                tk.Label(goal_info, text=f"{progress_rate:.1f}% ({status_text})", font=("맑은 고딕", 10, "bold"), bg="#a29bfe", fg=goal_color).pack(pady=(5, 10))
            
            # 기록 수 정보
            count_info = tk.Frame(summary_top, bg="#74b9ff", relief="solid", borderwidth=2)
            count_info.pack(side="right", fill="both", expand=True, padx=(10, 0))
            
            tk.Label(count_info, text="📊 기록 수", font=("맑은 고딕", 12, "bold"), bg="#74b9ff", fg="#2d3436").pack(pady=(10, 5))
            tk.Label(count_info, text=f"{len(filtered_records)}건", font=("맑은 고딕", 18, "bold"), bg="#74b9ff", fg="#2d3436").pack(pady=(0, 10))
            
            # 상세 기록 표시
            if not filtered_records:
                tk.Label(scrollable_frame, text=f"🔍 '{selected_filter}' 카테고리에 해당하는 기록이 없어요!",
                        font=("맑은 고딕", 14), bg="#fffef7", fg="#636e72").pack(pady=50)
                return
            
            # 기록 카드들 표시 (최신순)
            for i, record in enumerate(reversed(filtered_records)):
                # 원본 인덱스 찾기
                original_index = loaded_data.index(record)
                
                card_frame = tk.Frame(scrollable_frame, bg="#f8f9fa", relief="solid", borderwidth=2)
                card_frame.pack(fill="x", padx=15, pady=8)
                
                info_frame = tk.Frame(card_frame, bg="#f8f9fa")
                info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)
                
                first_line = tk.Frame(info_frame, bg="#f8f9fa")
                first_line.pack(fill="x", pady=(0, 5))
                
                tk.Label(first_line, text=f"📅 {format_date_with_weekday(record['날짜'])}", font=("맑은 고딕", 12, "bold"), bg="#f8f9fa", fg="#2d3436").pack(side="left")                
                tk.Label(first_line, text=f"🏷️ {record.get('카테고리', '미분류')}", font=("맑은 고딕", 12, "bold"), bg="#f8f9fa", fg="#0984e3").pack(side="right")
                tk.Label(info_frame, text=f"💰 {int(record['금액']):,}원", font=("맑은 고딕", 16, "bold"), bg="#f8f9fa", fg="#e17055").pack(anchor="w", pady=(0, 5))
                
                time_info = record.get('등록시간', '')
                if '수정시간' in record:
                    time_info += f" (수정: {record['수정시간']})"
                
                if time_info:
                    tk.Label(info_frame, text=f"⏰ {time_info}", font=("맑은 고딕", 9), bg="#f8f9fa", fg="#636e72").pack(anchor="w")
                
                # 버튼 프레임
                button_frame = tk.Frame(card_frame, bg="#f8f9fa")
                button_frame.pack(side="right", padx=15, pady=15)
                
                def make_edit_handler(idx, rec):
                    def handler():
                        edit_win = edit_record_window(idx, rec)
                        edit_win.parent_refresh = load_and_display_records
                    return handler
                
                def make_delete_handler(idx, rec):
                    def handler():
                        result = messagebox.askyesno(
                            "🗑️ 삭제 확인",
                            f"정말로 이 기록을 삭제하시겠어요?\n\n📅 {format_date_with_weekday(rec['날짜'])}\n🏷️ {rec.get('카테고리', '미분류')}\n💰 {int(rec['금액']):,}원",
                            icon='warning'
                        )
                        if result:
                            if delete_record(idx):
                                load_and_display_records()
                    return handler
                
                edit_btn = tk.Button(button_frame, text="✏️ 수정", command=make_edit_handler(original_index, record),
                                   bg="#fdcb6e", fg="#2d3436", font=("맑은 고딕", 10, "bold"), relief="solid",
                                   borderwidth=1, padx=15, pady=5, cursor="hand2")
                edit_btn.pack(pady=(0, 5))
                
                delete_btn = tk.Button(button_frame, text="🗑️ 삭제", command=make_delete_handler(original_index, record),
                                     bg="#fd79a8", fg="#2d3436", font=("맑은 고딕", 10, "bold"), relief="solid",
                                     borderwidth=1, padx=15, pady=5, cursor="hand2")
                delete_btn.pack()
            
        except Exception as e:
            tk.Label(scrollable_frame, text=f"❌ 데이터 로드 중 오류가 발생했어요: {e}",
                    font=("맑은 고딕", 12), bg="#fffef7", fg="#d63031").pack(pady=50)
    
    # 필터 버튼들
    button_frame = tk.Frame(filter_frame, bg="#fff9c4")
    button_frame.pack(side="right")
    
    filter_button = tk.Button(button_frame, text="🔍 보기", command=load_and_display_records, bg="#fdcb6e", fg="#2d3436",
                            font=("맑은 고딕", 10, "bold"), relief="solid", borderwidth=2, padx=20, pady=5, cursor="hand2")
    filter_button.pack(side="left", padx=(0, 5))
    
    def show_all():
        filter_combo.set("전체")
        load_and_display_records()
    
    all_button = tk.Button(button_frame, text="📋 전체", command=show_all, bg="#fd79a8", fg="#2d3436",
                         font=("맑은 고딕", 10, "bold"), relief="solid", borderwidth=2, padx=20, pady=5, cursor="hand2")
    all_button.pack(side="left", padx=(0, 5))
    
    refresh_button = tk.Button(button_frame, text="🔄 새로고침", command=load_and_display_records, bg="#74b9ff", fg="#2d3436",
                             font=("맑은 고딕", 10, "bold"), relief="solid", borderwidth=2, padx=20, pady=5, cursor="hand2")
    refresh_button.pack(side="left")
    
    # 마우스 휠 스크롤
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind("<MouseWheel>", _on_mousewheel)
    
    # 초기 로드
    load_and_display_records()

def click_save():
    """저장 버튼 클릭 시 실행되는 함수"""
    date = date_entry.get()
    amount = input_price.get().strip()
    category = category_combo.get()
    
    if save_record(date, amount, category):
        input_price.delete(0, tk.END)
        category_combo.set("")

# 메인 윈도우 생성
root = tk.Tk()
root.title("Sarin's 가계부🌻")
root.geometry("500x850")
root.configure(bg="#fff9c4")

# 상단 제목 프레임
title_frame = tk.Frame(root, bg="#ffeaa7", relief="solid", borderwidth=3, height=100)
title_frame.pack(fill="x", padx=20, pady=20)
title_frame.pack_propagate(False)

title_label = tk.Label(title_frame, text="Sarin's 가계부🌻", font=("맑은 고딕", 22, "bold"), fg="#2d3436", bg="#ffeaa7")
title_label.pack(expand=True)

# 메인 입력 프레임
main_frame = tk.Frame(root, bg="#fffef7", relief="solid", borderwidth=2)
main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

input_title = tk.Label(main_frame, text="✨ 새로운 기록 추가하기 ✨", font=("맑은 고딕", 16, "bold"), fg="#e17055", bg="#fffef7")
input_title.pack(pady=(25, 20))

input_container = tk.Frame(main_frame, bg="#fffef7")
input_container.pack(fill="x", padx=40)

# 날짜 선택 프레임
date_frame = tk.Frame(input_container, bg="#fff9c4", relief="solid", borderwidth=1)
date_frame.pack(fill="x", pady=(0, 15))

tk.Label(date_frame, text="📅 언제 사용했나요?", font=("맑은 고딕", 12, "bold"), bg="#fff9c4", fg="#2d3436").pack(anchor="w", padx=15, pady=(10, 5))

date_entry = DateEntry(date_frame, width=12, background='#fdcb6e', foreground='#2d3436', borderwidth=2, date_pattern='yyyy-mm-dd', font=("맑은 고딕", 11))
date_entry.pack(fill="x", padx=15, pady=(0, 10))

# 카테고리 선택 프레임
category_frame = tk.Frame(input_container, bg="#fff9c4", relief="solid", borderwidth=1)
category_frame.pack(fill="x", pady=(0, 15))

tk.Label(category_frame, text="🏷️ 어떤 종류인가요?", font=("맑은 고딕", 12, "bold"), bg="#fff9c4", fg="#2d3436").pack(anchor="w", padx=15, pady=(10, 5))

category_combo = ttk.Combobox(category_frame, values=["식비", "쇼핑", "교통비", "취미", "선물", "자기개발", "동아리", "기타"], state="readonly", font=("맑은 고딕", 11))
category_combo.pack(fill="x", padx=15, pady=(0, 10))

# 금액 입력 프레임
price_frame = tk.Frame(input_container, bg="#fff9c4", relief="solid", borderwidth=1)
price_frame.pack(fill="x", pady=(0, 15))

tk.Label(price_frame, text="💰 얼마를 사용했나요? (원)", font=("맑은 고딕", 12, "bold"), bg="#fff9c4", fg="#2d3436").pack(anchor="w", padx=15, pady=(10, 5))

input_price = tk.Entry(price_frame, font=("맑은 고딕", 14), relief="solid", borderwidth=1, justify="right", bg="#fffef7")
input_price.pack(fill="x", padx=15, pady=(0, 10))

# 버튼 프레임
button_frame = tk.Frame(main_frame, bg="#fffef7")
button_frame.pack(fill="x", padx=40, pady=30)

save_button = tk.Button(button_frame, text="💾 기록 저장하기", command=click_save, bg="#fd79a8", fg="#2d3436",
                       font=("맑은 고딕", 14, "bold"), relief="solid", borderwidth=2, padx=30, pady=12, cursor="hand2")
save_button.pack(fill="x", pady=(0, 10))

show_button = tk.Button(button_frame, text="📊 내 기록 보러가기", command=show_records, bg="#74b9ff", fg="#2d3436",
                       font=("맑은 고딕", 14, "bold"), relief="solid", borderwidth=2, padx=30, pady=12, cursor="hand2")
show_button.pack(fill="x", pady=(0, 10))

goal_button = tk.Button(button_frame, text="🎯 목표 설정하기", command=show_goal_setting, bg="#a29bfe", fg="#2d3436",
                       font=("맑은 고딕", 14, "bold"), relief="solid", borderwidth=2, padx=30, pady=12, cursor="hand2")
goal_button.pack(fill="x")

# 하단 팁
tip_frame = tk.Frame(root, bg="#fdcb6e", relief="solid", borderwidth=2)
tip_frame.pack(fill="x", padx=20, pady=(0, 20))

info_label = tk.Label(tip_frame, text="💡 꿀팁: 금액은 숫자만 입력하세요! (예: 5000) 🌻\n✏️ 기록 보기에서 수정/삭제도 가능해요! 📝\n🎯 목표 설정으로 지출을 계획적으로 관리하세요! 💪",
                     font=("맑은 고딕", 10, "bold"), fg="#2d3436", bg="#fdcb6e", justify="center")
info_label.pack(pady=10)

# 엔터키 저장
def on_enter(event):
    click_save()

input_price.bind('<Return>', on_enter)

# 앱 실행
if __name__ == "__main__":
    root.mainloop()