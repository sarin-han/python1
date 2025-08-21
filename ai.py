import tkinter as tk
from tkcalendar import DateEntry
import os
import json
from tkinter import ttk, messagebox
from datetime import datetime

def save_record(date, amount, category):
    """가계부 기록을 저장하는 함수"""
    try:
        # 금액이 숫자인지 확인
        if not amount.isdigit():
            messagebox.showerror("⚠️ 입력 오류", "금액은 숫자만 입력해주세요! 😊")
            return False
            
        # 카테고리가 선택되었는지 확인
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
        # 금액이 숫자인지 확인
        if not amount.isdigit():
            messagebox.showerror("⚠️ 입력 오류", "금액은 숫자만 입력해주세요! 😊")
            return False
            
        # 카테고리가 선택되었는지 확인
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

def edit_record_window(index, record):
    """기록 수정 창을 여는 함수"""
    edit_window = tk.Toplevel()
    edit_window.title(f"✏️ 기록 수정하기")
    edit_window.geometry("400x500")
    edit_window.configure(bg="#fff9c4")
    edit_window.grab_set()  # 모달 창으로 만들기
    
    # 제목
    title_label = tk.Label(
        edit_window,
        text="✏️ 기록 수정하기",
        font=("맑은 고딕", 18, "bold"),
        fg="#e17055",
        bg="#fff9c4"
    )
    title_label.pack(pady=20)
    
    # 입력 프레임
    input_frame = tk.Frame(edit_window, bg="#fffef7", relief="solid", borderwidth=2)
    input_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    # 날짜 입력
    date_frame = tk.Frame(input_frame, bg="#fff9c4", relief="solid", borderwidth=1)
    date_frame.pack(fill="x", padx=20, pady=20)
    
    tk.Label(
        date_frame, 
        text="📅 날짜", 
        font=("맑은 고딕", 12, "bold"), 
        bg="#fff9c4",
        fg="#2d3436"
    ).pack(anchor="w", padx=15, pady=(10, 5))
    
    edit_date_entry = DateEntry(
        date_frame,
        width=12,
        background='#fdcb6e',
        foreground='#2d3436',
        borderwidth=2,
        date_pattern='yyyy-mm-dd',
        font=("맑은 고딕", 11)
    )
    # 기존 날짜로 설정
    try:
        edit_date_entry.set_date(datetime.strptime(record['날짜'], '%Y-%m-%d').date())
    except:
        pass
    edit_date_entry.pack(fill="x", padx=15, pady=(0, 10))
    
    # 카테고리 입력
    category_frame = tk.Frame(input_frame, bg="#fff9c4", relief="solid", borderwidth=1)
    category_frame.pack(fill="x", padx=20, pady=(0, 20))
    
    tk.Label(
        category_frame, 
        text="🏷️ 카테고리", 
        font=("맑은 고딕", 12, "bold"), 
        bg="#fff9c4",
        fg="#2d3436"
    ).pack(anchor="w", padx=15, pady=(10, 5))
    
    edit_category_combo = ttk.Combobox(
        category_frame,
        values=["식비", "쇼핑", "교통비", "취미", "선물", "자기개발", "동아리", "기타"],
        state="readonly",
        font=("맑은 고딕", 11)
    )
    edit_category_combo.set(record.get('카테고리', ''))
    edit_category_combo.pack(fill="x", padx=15, pady=(0, 10))
    
    # 금액 입력
    price_frame = tk.Frame(input_frame, bg="#fff9c4", relief="solid", borderwidth=1)
    price_frame.pack(fill="x", padx=20, pady=(0, 20))
    
    tk.Label(
        price_frame, 
        text="💰 금액 (원)", 
        font=("맑은 고딕", 12, "bold"), 
        bg="#fff9c4",
        fg="#2d3436"
    ).pack(anchor="w", padx=15, pady=(10, 5))
    
    edit_amount_entry = tk.Entry(
        price_frame,
        font=("맑은 고딕", 14),
        relief="solid",
        borderwidth=1,
        justify="right",
        bg="#fffef7"
    )
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
            # 부모 창 새로고침을 위해 전역 변수 사용
            if hasattr(edit_window, 'parent_refresh'):
                edit_window.parent_refresh()
    
    def cancel_edit():
        edit_window.destroy()
    
    # 저장 버튼
    save_btn = tk.Button(
        button_frame,
        text="💾 저장하기",
        command=save_changes,
        bg="#00b894",
        fg="white",
        font=("맑은 고딕", 12, "bold"),
        relief="solid",
        borderwidth=2,
        padx=30,
        pady=8,
        cursor="hand2"
    )
    save_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
    
    # 취소 버튼
    cancel_btn = tk.Button(
        button_frame,
        text="❌ 취소",
        command=cancel_edit,
        bg="#ddd",
        fg="#2d3436",
        font=("맑은 고딕", 12, "bold"),
        relief="solid",
        borderwidth=2,
        padx=30,
        pady=8,
        cursor="hand2"
    )
    cancel_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
    
    # 엔터키로 저장
    def on_enter(event):
        save_changes()
    
    edit_amount_entry.bind('<Return>', on_enter)
    
    return edit_window

def click_save():
    """저장 버튼 클릭 시 실행되는 함수"""
    date = date_entry.get()
    amount = input_price.get().strip()
    category = category_combo.get()
    
    if save_record(date, amount, category):
        # 저장 성공시 입력창 초기화
        input_price.delete(0, tk.END)
        category_combo.set("")

def show_records():
    """저장된 기록을 보여주는 함수"""
    new_window = tk.Toplevel(root)
    new_window.title("🌻 내 가계부 내역")
    new_window.geometry("800x700")
    new_window.configure(bg="#fff9c4")
    
    # 상단 큰 정보 패널
    info_panel = tk.Frame(new_window, bg="#ffeaa7", relief="solid", borderwidth=2)
    info_panel.pack(fill="x", padx=20, pady=20)
    
    # 제목
    title_label = tk.Label(
        info_panel, 
        text="🌻 내 가계부 요약",
        font=("맑은 고딕", 20, "bold"),
        fg="#2d3436", 
        bg="#ffeaa7"
    )
    title_label.pack(pady=(15, 10))
    
    # 요약 정보 프레임
    summary_frame = tk.Frame(info_panel, bg="#ffeaa7")
    summary_frame.pack(fill="x", padx=20, pady=(0, 15))
    
    # 필터 선택 프레임
    filter_frame = tk.Frame(new_window, bg="#fff9c4")
    filter_frame.pack(fill="x", padx=20, pady=10)
    
    filter_label = tk.Label(
        filter_frame, 
        text="🔍 보고싶은 카테고리:", 
        font=("맑은 고딕", 12, "bold"), 
        bg="#fff9c4",
        fg="#2d3436"
    )
    filter_label.pack(side="left", padx=(0, 10))
    
    filter_combo = ttk.Combobox(
        filter_frame, 
        values=["전체", "식비", "쇼핑", "교통비", "취미", "선물", "자기개발", "동아리", "기타"],
        state="readonly",
        width=15,
        font=("맑은 고딕", 11)
    )
    filter_combo.pack(side="left", padx=(0, 10))
    filter_combo.set("전체")
    
    # 상세 기록 프레임
    detail_frame = tk.Frame(new_window, bg="#fff9c4")
    detail_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
    
    # 상세 기록 제목
    detail_title = tk.Label(
        detail_frame,
        text="📝 상세 기록",
        font=("맑은 고딕", 14, "bold"),
        bg="#fff9c4",
        fg="#2d3436"
    )
    detail_title.pack(anchor="w", pady=(0, 10))
    
    # 스크롤 가능한 프레임 생성
    canvas = tk.Canvas(detail_frame, bg="#fffef7")
    scrollbar = ttk.Scrollbar(detail_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#fffef7")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def load_and_display_records():
        """기록을 로드하고 화면에 표시"""
        # 기존 요약 정보 지우기
        for widget in summary_frame.winfo_children():
            widget.destroy()
            
        # 스크롤 프레임 내용 지우기
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        
        if not os.path.exists("data.json"):
            # 요약 정보
            no_data_label = tk.Label(
                summary_frame,
                text="💡 아직 기록이 없어요!\n메인 화면에서 첫 기록을 추가해보세요 🌟",
                font=("맑은 고딕", 14),
                fg="#636e72",
                bg="#ffeaa7",
                justify="center"
            )
            no_data_label.pack(pady=20)
            
            tk.Label(
                scrollable_frame,
                text="🌻 새로운 가계부를 시작해보세요!",
                font=("맑은 고딕", 16),
                bg="#fffef7",
                fg="#636e72"
            ).pack(pady=50)
            return
            
        try:
            with open("data.json", "r", encoding="utf-8") as file:
                loaded_data = json.load(file)
                
            if not loaded_data:
                # 빈 데이터
                no_data_label = tk.Label(
                    summary_frame,
                    text="💡 저장된 기록이 없어요!",
                    font=("맑은 고딕", 14),
                    fg="#636e72",
                    bg="#ffeaa7"
                )
                no_data_label.pack(pady=20)
                
                tk.Label(
                    scrollable_frame,
                    text="🌻 첫 기록을 추가해보세요!",
                    font=("맑은 고딕", 16),
                    bg="#fffef7",
                    fg="#636e72"
                ).pack(pady=50)
                return
                
            selected_filter = filter_combo.get()
            filtered_records = []
            filtered_indices = []
            total_amount = 0
            
            # 필터링 및 합계 계산
            for i, record in enumerate(loaded_data):
                if selected_filter == "전체" or record.get('카테고리') == selected_filter:
                    filtered_records.append(record)
                    filtered_indices.append(i)
                    total_amount += int(record.get('금액', 0))
            
            # 카테고리별 통계 계산
            category_stats = {}
            total_records = len(loaded_data)
            grand_total = 0
            
            for record in loaded_data:
                cat = record.get('카테고리', '미분류')
                amount = int(record.get('금액', 0))
                grand_total += amount
                
                if cat not in category_stats:
                    category_stats[cat] = {'count': 0, 'amount': 0}
                category_stats[cat]['count'] += 1
                category_stats[cat]['amount'] += amount
            
            # 상단 요약 정보 표시
            summary_top = tk.Frame(summary_frame, bg="#ffeaa7")
            summary_top.pack(fill="x", pady=(0, 15))
            
            # 전체 통계
            total_info = tk.Frame(summary_top, bg="#fdcb6e", relief="solid", borderwidth=2)
            total_info.pack(side="left", fill="both", expand=True, padx=(0, 10))
            
            tk.Label(
                total_info,
                text="💰 전체 사용금액",
                font=("맑은 고딕", 12, "bold"),
                bg="#fdcb6e",
                fg="#2d3436"
            ).pack(pady=(10, 5))
            
            tk.Label(
                total_info,
                text=f"{grand_total:,}원",
                font=("맑은 고딕", 18, "bold"),
                bg="#fdcb6e",
                fg="#d63031"
            ).pack(pady=(0, 10))
            
            # 기록 수
            count_info = tk.Frame(summary_top, bg="#fd79a8", relief="solid", borderwidth=2)
            count_info.pack(side="left", fill="both", expand=True, padx=5)
            
            tk.Label(
                count_info,
                text="📊 총 기록 수",
                font=("맑은 고딕", 12, "bold"),
                bg="#fd79a8",
                fg="#2d3436"
            ).pack(pady=(10, 5))
            
            tk.Label(
                count_info,
                text=f"{total_records}건",
                font=("맑은 고딕", 18, "bold"),
                bg="#fd79a8",
                fg="#2d3436"
            ).pack(pady=(0, 10))
            
            # 선택된 카테고리 정보
            selected_info = tk.Frame(summary_top, bg="#74b9ff", relief="solid", borderwidth=2)
            selected_info.pack(side="left", fill="both", expand=True, padx=(10, 0))
            
            tk.Label(
                selected_info,
                text=f"🏷️ {selected_filter}",
                font=("맑은 고딕", 12, "bold"),
                bg="#74b9ff",
                fg="#2d3436"
            ).pack(pady=(10, 5))
            
            if filtered_records:
                tk.Label(
                    selected_info,
                    text=f"{total_amount:,}원",
                    font=("맑은 고딕", 18, "bold"),
                    bg="#74b9ff",
                    fg="#2d3436"
                ).pack(pady=(0, 5))
                
                tk.Label(
                    selected_info,
                    text=f"({len(filtered_records)}건)",
                    font=("맑은 고딕", 10),
                    bg="#74b9ff",
                    fg="#636e72"
                ).pack(pady=(0, 10))
            else:
                tk.Label(
                    selected_info,
                    text="0원 (0건)",
                    font=("맑은 고딕", 14),
                    bg="#74b9ff",
                    fg="#636e72"
                ).pack(pady=(0, 10))
            
            # 상세 기록 표시
            if not filtered_records:
                tk.Label(
                    scrollable_frame,
                    text=f"🔍 '{selected_filter}' 카테고리에 해당하는 기록이 없어요!",
                    font=("맑은 고딕", 14),
                    bg="#fffef7",
                    fg="#636e72"
                ).pack(pady=50)
                return
            
            # 기록 카드들 표시 (최신순)
            for i, (record, original_index) in enumerate(zip(reversed(filtered_records), reversed(filtered_indices))):
                # 각 기록에 대한 카드 프레임
                card_frame = tk.Frame(scrollable_frame, bg="#f8f9fa", relief="solid", borderwidth=2)
                card_frame.pack(fill="x", padx=15, pady=8)
                
                # 기록 정보 프레임
                info_frame = tk.Frame(card_frame, bg="#f8f9fa")
                info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)
                
                # 첫 번째 줄: 날짜와 카테고리
                first_line = tk.Frame(info_frame, bg="#f8f9fa")
                first_line.pack(fill="x", pady=(0, 5))
                
                tk.Label(
                    first_line,
                    text=f"📅 {record['날짜']}",
                    font=("맑은 고딕", 12, "bold"),
                    bg="#f8f9fa",
                    fg="#2d3436"
                ).pack(side="left")
                
                tk.Label(
                    first_line,
                    text=f"🏷️ {record.get('카테고리', '미분류')}",
                    font=("맑은 고딕", 12, "bold"),
                    bg="#f8f9fa",
                    fg="#0984e3"
                ).pack(side="right")
                
                # 두 번째 줄: 금액
                tk.Label(
                    info_frame,
                    text=f"💰 {int(record['금액']):,}원",
                    font=("맑은 고딕", 16, "bold"),
                    bg="#f8f9fa",
                    fg="#e17055"
                ).pack(anchor="w", pady=(0, 5))
                
                # 세 번째 줄: 등록/수정 시간
                time_info = record.get('등록시간', '')
                if '수정시간' in record:
                    time_info += f" (수정: {record['수정시간']})"
                
                if time_info:
                    tk.Label(
                        info_frame,
                        text=f"⏰ {time_info}",
                        font=("맑은 고딕", 9),
                        bg="#f8f9fa",
                        fg="#636e72"
                    ).pack(anchor="w")
                
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
                            f"정말로 이 기록을 삭제하시겠어요?\n\n📅 {rec['날짜']}\n🏷️ {rec.get('카테고리', '미분류')}\n💰 {int(rec['금액']):,}원",
                            icon='warning'
                        )
                        if result:
                            if delete_record(idx):
                                load_and_display_records()
                    return handler
                
                # 수정 버튼
                edit_btn = tk.Button(
                    button_frame,
                    text="✏️ 수정",
                    command=make_edit_handler(original_index, record),
                    bg="#fdcb6e",
                    fg="#2d3436",
                    font=("맑은 고딕", 10, "bold"),
                    relief="solid",
                    borderwidth=1,
                    padx=15,
                    pady=5,
                    cursor="hand2"
                )
                edit_btn.pack(pady=(0, 5))
                
                # 삭제 버튼
                delete_btn = tk.Button(
                    button_frame,
                    text="🗑️ 삭제",
                    command=make_delete_handler(original_index, record),
                    bg="#fd79a8",
                    fg="#2d3436",
                    font=("맑은 고딕", 10, "bold"),
                    relief="solid",
                    borderwidth=1,
                    padx=15,
                    pady=5,
                    cursor="hand2"
                )
                delete_btn.pack()
            
        except Exception as e:
            tk.Label(
                scrollable_frame,
                text=f"❌ 데이터 로드 중 오류가 발생했어요: {e}",
                font=("맑은 고딕", 12),
                bg="#fffef7",
                fg="#d63031"
            ).pack(pady=50)
    
    # 필터 적용 함수
    def apply_filter():
        load_and_display_records()
    
    # 버튼 프레임
    button_frame = tk.Frame(filter_frame, bg="#fff9c4")
    button_frame.pack(side="right")
    
    # 필터 버튼
    filter_button = tk.Button(
        button_frame,
        text="🔍 보기",
        command=apply_filter,
        bg="#fdcb6e",
        fg="#2d3436",
        font=("맑은 고딕", 10, "bold"),
        relief="solid",
        borderwidth=2,
        padx=20,
        pady=5,
        cursor="hand2"
    )
    filter_button.pack(side="left", padx=(0, 5))
    
    # 전체 기록 버튼
    def show_all():
        filter_combo.set("전체")
        apply_filter()
    
    all_button = tk.Button(
        button_frame,
        text="📋 전체",
        command=show_all,
        bg="#fd79a8",
        fg="#2d3436",
        font=("맑은 고딕", 10, "bold"),
        relief="solid",
        borderwidth=2,
        padx=20,
        pady=5,
        cursor="hand2"
    )
    all_button.pack(side="left")
    
    # 새로고침 버튼
    refresh_button = tk.Button(
        button_frame,
        text="🔄 새로고침",
        command=load_and_display_records,
        bg="#74b9ff",
        fg="#2d3436",
        font=("맑은 고딕", 10, "bold"),
        relief="solid",
        borderwidth=2,
        padx=20,
        pady=5,
        cursor="hand2"
    )
    refresh_button.pack(side="left", padx=(5, 0))
    
    # 마우스 휠 스크롤 바인딩
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind("<MouseWheel>", _on_mousewheel)
    
    # 초기 로드
    load_and_display_records()

# 메인 윈도우 생성
root = tk.Tk()
root.title("Sarin's 가계부🌻")
root.geometry("500x850")
root.configure(bg="#fff9c4")

# 상단 제목 프레임s
title_frame = tk.Frame(root, bg="#ffeaa7", relief="solid", borderwidth=3, height=100)
title_frame.pack(fill="x", padx=20, pady=20)
title_frame.pack_propagate(False)

# 제목
title_label = tk.Label(
    title_frame,
    text="Sarin's 가계부🌻",
    font=("맑은 고딕", 22, "bold"),
    fg="#2d3436",
    bg="#ffeaa7"
)
title_label.pack(expand=True)

# 메인 입력 프레임
main_frame = tk.Frame(root, bg="#fffef7", relief="solid", borderwidth=2)
main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

# 입력 섹션 제목
input_title = tk.Label(
    main_frame,
    text="✨ 새로운 기록 추가하기 ✨",
    font=("맑은 고딕", 16, "bold"),
    fg="#e17055",
    bg="#fffef7"
)
input_title.pack(pady=(25, 20))

# 입력 필드들을 담을 컨테이너
input_container = tk.Frame(main_frame, bg="#fffef7")
input_container.pack(fill="x", padx=40)

# 날짜 선택 프레임
date_frame = tk.Frame(input_container, bg="#fff9c4", relief="solid", borderwidth=1)
date_frame.pack(fill="x", pady=(0, 15))

tk.Label(
    date_frame, 
    text="📅 언제 사용했나요?", 
    font=("맑은 고딕", 12, "bold"), 
    bg="#fff9c4",
    fg="#2d3436"
).pack(anchor="w", padx=15, pady=(10, 5))

date_entry = DateEntry(
    date_frame,
    width=12,
    background='#fdcb6e',
    foreground='#2d3436',
    borderwidth=2,
    date_pattern='yyyy-mm-dd',
    font=("맑은 고딕", 11)
)
date_entry.pack(fill="x", padx=15, pady=(0, 10))

# 카테고리 선택 프레임
category_frame = tk.Frame(input_container, bg="#fff9c4", relief="solid", borderwidth=1)
category_frame.pack(fill="x", pady=(0, 15))

tk.Label(
    category_frame, 
    text="🏷️ 어떤 종류인가요?", 
    font=("맑은 고딕", 12, "bold"), 
    bg="#fff9c4",
    fg="#2d3436"
).pack(anchor="w", padx=15, pady=(10, 5))

category_combo = ttk.Combobox(
    category_frame,
    values=["식비", "쇼핑", "교통비", "취미", "선물", "자기개발", "동아리", "기타"],
    state="readonly",
    font=("맑은 고딕", 11)
)
category_combo.pack(fill="x", padx=15, pady=(0, 10))

# 금액 입력 프레임
price_frame = tk.Frame(input_container, bg="#fff9c4", relief="solid", borderwidth=1)
price_frame.pack(fill="x", pady=(0, 15))

tk.Label(
    price_frame, 
    text="💰 얼마를 사용했나요? (원)", 
    font=("맑은 고딕", 12, "bold"), 
    bg="#fff9c4",
    fg="#2d3436"
).pack(anchor="w", padx=15, pady=(10, 5))

input_price = tk.Entry(
    price_frame,
    font=("맑은 고딕", 14),
    relief="solid",
    borderwidth=1,
    justify="right",
    bg="#fffef7"
)
input_price.pack(fill="x", padx=15, pady=(0, 10))

# 버튼 프레임
button_frame = tk.Frame(main_frame, bg="#fffef7")
button_frame.pack(fill="x", padx=40, pady=30)

# 기록 추가 버튼
save_button = tk.Button(
    button_frame,
    text="💾 기록 저장하기",
    command=click_save,
    bg="#fd79a8",
    fg="#2d3436",
    font=("맑은 고딕", 14, "bold"),
    relief="solid",
    borderwidth=2,
    padx=30,
    pady=12,
    cursor="hand2"
)
save_button.pack(fill="x", pady=(0, 10))

# 기록 보기 버튼
show_button = tk.Button(
    button_frame,
    text="📊 내 기록 보러가기",
    command=show_records,
    bg="#74b9ff",
    fg="#2d3436",
    font=("맑은 고딕", 14, "bold"),
    relief="solid",
    borderwidth=2,
    padx=30,
    pady=12,
    cursor="hand2"
)
show_button.pack(fill="x")

# 하단 귀여운 팁
tip_frame = tk.Frame(root, bg="#fdcb6e", relief="solid", borderwidth=2)
tip_frame.pack(fill="x", padx=20, pady=(0, 20))

info_label = tk.Label(
    tip_frame,
    text="💡 꿀팁: 금액은 숫자만 입력하세요! (예: 5000) 🌻\n✏️ 기록 보기에서 수정/삭제도 가능해요! 📝",
    font=("맑은 고딕", 10, "bold"),
    fg="#2d3436",
    bg="#fdcb6e",
    justify="center"
)
info_label.pack(pady=10)

# 엔터키로 저장 기능
def on_enter(event):
    click_save()

input_price.bind('<Return>', on_enter)

root.mainloop()