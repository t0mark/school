import random
from collections import defaultdict


def assign_groups(members, leaders, same_group, diff_group, num_groups):
    #             전인원   리더     같은 그룹   다른 그룹   그룹 수

    # 단계 1: 초기 빈 그룹 생성
    groups = defaultdict(list)
    
    # 이미 할당된 멤버를 추적하여 중복을 방지
    assigned_members = set()

    # 단계 2: 리더를 그룹에 할당, 각 그룹마다 여러 리더 가능
    for i, leader_group in enumerate(leaders):
        groups[i % num_groups].extend(leader_group)
        assigned_members.update(leader_group)

    # 단계 3: 같은 그룹에 속해야 하는 멤버들 할당
    for group in same_group:
        # 그룹의 멤버 중 하나라도 이미 할당된 경우 (예: 리더)
        assigned_group_index = None
        for member in group:
            for i in range(num_groups):
                if member in groups[i]:
                    assigned_group_index = i
                    break
            if assigned_group_index is not None:
                break

        # 리더가 있는 그룹에 전체 same_group 할당
        if assigned_group_index is not None:
            for member in group:
                if member not in assigned_members:
                    groups[assigned_group_index].append(member)
                    assigned_members.add(member)
        else:
            # 그렇지 않은 경우 무작위로 후보 그룹 중 하나를 선택하여 할당
            min_group_size = min(len(groups[i]) for i in range(num_groups))
            candidate_groups = [i for i in range(num_groups) if len(groups[i]) == min_group_size]
            chosen_group = random.choice(candidate_groups)  # 후보 그룹 중 하나를 무작위 선택
            groups[chosen_group].extend(group)
            assigned_members.update(group)

    # 단계 4: 이미 할당된 멤버를 멤버 목록에서 제거
    remaining_members = [m for m in members if m not in assigned_members]

    # 단계 5: 남은 멤버를 셔플하고 할당, diff_group 제약을 유지하면서 다른 그룹에 멤버 배치
    random.shuffle(remaining_members)
    diff_group_sets = [set() for _ in range(len(diff_group))]

    for member in remaining_members:
        # diff_group 제약을 유지하면서 최소 크기의 그룹 찾기
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


    # 그룹을 리스트로 변환하여 정렬된 순서로 쉽게 표시
    return [groups[i] for i in range(num_groups)]


# 조장 랜덤 편성
def leader_groups(leader_members, num_groups):
    groups = []

    for _ in range(num_groups):
        gropus.append([])
    
    random.suffle(leader_members)
    for i, member in enumerate(leader_members):
        gropus[i % num_groups].append(member)

    return groups


# 예제 사용
members = [
    '김강민', '김주헌', '송한얼', '양성제', '양현웅', '이다혁', '이유림', '이재겸', '고다견', '박민건', 
    '유민준', '전수완', '공민석', '박종현', '이재혁', '정재윤', '곽정인', '선동호', '이정석', '홍현진', 
    '김동현', '송경민', '이현빈', '김중기', '심재상', '임수현', '박근수', '양승미', '장현석'
]
same_group  = [['공민석', '박근수'], ['이다혁', '김주헌', '송경민', '임수현', '이재혁'], ['양성제', '김동현'], ['이재겸', '선동호']]
diff_group = [['양성제', '곽정인'], ['김중기', '전수완']]
random_diff = []
leaders  = [['이유림', '양현웅'], ['이다혁', '김주헌'], ['김강민', '양성제'], ['송한얼', '이재겸']]
# leader_members = ['이유림', '양현웅', '이다혁', '김주헌', '양성제', '김강민', '송한얼', '이재겸']

num_groups = 4

# leaders = leader_groups(leader_members, num_groups)
groups = assign_groups(members, leaders, same_group, diff_group, num_groups)

for i, group in enumerate(groups):
    print(f"{i+1}조: {group}")
