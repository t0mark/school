import tkinter as tk
from tkinter import ttk
import random
import json
from collections import defaultdict


def parse_settings(file_path):
    """settings.txt 파일을 JSON 형식으로 읽고 주석을 무시"""
    lines = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith("#"):
                continue  # 빈 줄이나 주석 무시
            lines.append(stripped_line)
    json_content = "\n".join(lines)
    return json.loads(json_content)

def assign_groups(members, leaders, same_group, diff_group, num_groups):
    """멤버를 그룹으로 랜덤 배치"""
    groups = defaultdict(list)
    assigned_members = set()

    # 단계 1: 리더 배치
    for i, leader_group in enumerate(leaders):
        groups[i % num_groups].extend(leader_group)
        assigned_members.update(leader_group)

    # 단계 2: 같은 그룹 멤버 배치
    for group in same_group:
        assigned_group_index = None
        for member in group:
            for i in range(num_groups):
                if member in groups[i]:
                    assigned_group_index = i
                    break
            if assigned_group_index is not None:
                break

        if assigned_group_index is not None:
            for member in group:
                if member not in assigned_members:
                    groups[assigned_group_index].append(member)
                    assigned_members.add(member)
        else:
            min_group_size = min(len(groups[i]) for i in range(num_groups))
            candidate_groups = [i for i in range(num_groups) if len(groups[i]) == min_group_size]
            chosen_group = random.choice(candidate_groups)
            groups[chosen_group].extend(group)
            assigned_members.update(group)

    # 단계 3: 남은 멤버 배치
    remaining_members = [m for m in members if m not in assigned_members]
    random.shuffle(remaining_members)
    diff_group_sets = [set() for _ in range(len(diff_group))]

    for member in remaining_members:
        min_group_size = min(len(groups[i]) for i in range(num_groups))
        candidate_groups = [i for i in range(num_groups) if len(groups[i]) == min_group_size]

        assigned = False
        for i in candidate_groups:
            if all(member not in diff_group[j] or i not in diff_group_sets[j] for j in range(len(diff_group))):
                groups[i].append(member)
                for j in range(len(diff_group)):
                    if member in diff_group[j]:
                        diff_group_sets[j].add(i)
                assigned = True
                break

        if not assigned:
            raise ValueError(f"Could not assign {member} due to diff_group constraints.")

    return [groups[i] for i in range(num_groups)]


def generate_groups():
    """그룹 생성 및 결과 표시"""
    try:
        settings = parse_settings("settings.txt")
        members = settings["members"]
        leaders = settings["leaders"]
        same_group = settings["same_group"]
        diff_group = settings["diff_group"]
        num_groups = settings["num_groups"]

        groups = assign_groups(members, leaders, same_group, diff_group, num_groups)

        # 테이블 초기화
        for row in tree.get_children():
            tree.delete(row)

        # 결과 추가
        for i, group in enumerate(groups):
            tree.insert("", "end", values=(f"{i + 1}조", ", ".join(group)))

        result_label.config(text="그룹 생성이 완료되었습니다!")

    except Exception as e:
        result_label.config(text=f"오류: {e}")


# GUI 설정
root = tk.Tk()
root.title("조 편성")
root.geometry("600x400")
root.configure(bg="white")

# 테이블 (Treeview)
tree = ttk.Treeview(root, columns=("Group", "Members"), show="headings", height=15)
tree.heading("Group", text="Group")
tree.heading("Members", text="Members")
tree.column("Group", width=100, anchor="center")
tree.column("Members", width=400, anchor="w")
tree.pack(pady=20)

# 버튼
generate_button = ttk.Button(root, text="그룹 생성", command=generate_groups)
generate_button.pack(pady=5)

# 오류 메시지 표시
result_label = tk.Label(root, text="", fg="red", bg="white")
result_label.pack()

root.mainloop()
