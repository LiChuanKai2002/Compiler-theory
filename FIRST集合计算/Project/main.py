import tkinter as tk
from tkinter import scrolledtext


def create_window():
    root = tk.Tk()
    root.title("LL(1)文法判断器")

    # 创建左侧框架
    left_frame = tk.Frame(root)
    left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    input_label = tk.Label(left_frame,
                           text="请输入文法的产生式(每行一个产生式，格式:非终结符->产生式|产生式，点击按钮进行计算)：",
                           fg="blue", font=("Arial", 12))
    input_label.pack()

    global text
    text = scrolledtext.ScrolledText(left_frame, height=10, width=15, font=("Verdana", 12))
    text.pack(expand=True, fill="both")

    calculate_button = tk.Button(left_frame, text="开始判断", command=process_input, fg="blue", font=("Arial", 12))
    calculate_button.pack(pady=10)

    # 创建右侧框架
    right_frame = tk.Frame(root)
    right_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10, ipadx=5)

    # 创建右侧框架中的文本结果显示区域
    result_frame = tk.Frame(right_frame)
    result_frame.pack(expand=True, fill="both")

    global first_result
    first_label = tk.Label(result_frame, text="FIRST 集合：", fg="red", font=("Arial", 12))
    first_label.pack()
    first_result = scrolledtext.ScrolledText(result_frame, height=5, width=40, state="disabled", font=("Verdana", 12))
    first_result.pack(expand=True, fill="both")

    global follow_result
    follow_label = tk.Label(result_frame, text="FOLLOW 集合：", fg="red", font=("Arial", 12))
    follow_label.pack()
    follow_result = scrolledtext.ScrolledText(result_frame, height=5, width=40, state="disabled", font=("Verdana", 12))
    follow_result.pack(expand=True, fill="both")

    global select_result
    select_label = tk.Label(result_frame, text="SELECT 集合：", fg="red", font=("Arial", 12))
    select_label.pack()
    select_result = scrolledtext.ScrolledText(result_frame, height=10, width=40, state="disabled", font=("Verdana", 12))
    select_result.pack(expand=True, fill="both")

    global conflict_result
    conflict_label = tk.Label(right_frame, text="LL(1)判断结果：", fg="red", font=("Arial", 12))
    conflict_label.pack()
    conflict_result = scrolledtext.ScrolledText(right_frame, height=5, width=40, state="disabled", font=("Verdana", 12))
    conflict_result.pack(expand=True, fill="both", pady=(0, 10))

    root.mainloop()


def process_input():
    productions = {}
    input_text = text.get("1.0", tk.END).strip().split("\n")
    for line in input_text:
        if line.strip() == '':
            continue
        left, right = line.split('->')
        left = left.strip()
        if left not in productions:
            productions[left] = []
        productions[left].extend([prod.strip() for prod in right.split('|')])

    firsts = calculate_first_in(productions)
    follows = calculate_follow_in(productions, firsts)
    selects = calculate_select_in(productions, firsts, follows)

    first_text = "\n".join(
        [f"FIRST({non_terminal}) = {{ {', '.join(first)} }}" for non_terminal, first in firsts.items()])
    follow_text = "\n".join(
        [f"FOLLOW({non_terminal}) = {{ {', '.join(follow)} }}" for non_terminal, follow in follows.items()])
    select_text = "\n".join([f"SELECT({key}) = {{ {', '.join(select)} }}" for key, select in selects.items()])

    first_result.config(state="normal")
    first_result.delete("1.0", tk.END)
    first_result.insert(tk.END, first_text)
    first_result.config(state="disabled")

    follow_result.config(state="normal")
    follow_result.delete("1.0", tk.END)
    follow_result.insert(tk.END, follow_text)
    follow_result.config(state="disabled")

    select_result.config(state="normal")
    select_result.delete("1.0", tk.END)
    select_result.insert(tk.END, select_text)
    select_result.config(state="disabled")

    conflict_productions = is_ll1(selects)
    if conflict_productions:
        conflict_info = "该文法不是LL(1)型文法，存在以下冲突:\n"
        conflict_text = "\n".join(
            [f"\t• 产生式 {conflict[0][0]}->{conflict[0][1]} 与 {conflict[1][0]}->{conflict[1][1]} 冲突" for conflict in
             conflict_productions])
        conflict_info += conflict_text

        # 显示冲突信息
        conflict_result.config(state="normal")
        conflict_result.delete("1.0", tk.END)
        conflict_result.insert(tk.END, conflict_info)
        conflict_result.tag_add("red", "1.0", "end")
        conflict_result.tag_config("red", foreground="red")
        conflict_result.config(state="disabled")
    else:
        # 如果是LL(1)型文法，清除冲突信息
        conflict_result.config(state="normal")
        conflict_result.delete("1.0", tk.END)
        conflict_result.insert(tk.END, "该文法是LL(1)型文法")
        conflict_result.tag_add("red", "1.0", "end")
        conflict_result.tag_config("red", foreground="red")
        conflict_result.config(state="disabled")


def calculate_first_in(productions):
    firsts = {}
    completed = {}

    for non_terminal in productions:
        firsts[non_terminal] = set()
        completed[non_terminal] = False

    def calculate_first(non_terminal):
        if completed[non_terminal]:
            return firsts[non_terminal]

        visited = set()
        stack = [non_terminal]

        while stack:
            current = stack.pop()
            if current in visited:
                continue

            visited.add(current)

            for production in productions[current]:
                if production:
                    double_char = production[0:3]
                    if double_char in terminal_e:
                        firsts[non_terminal].add(double_char)
                    else:
                        first_char = production[0]
                        if (first_char.islower() or first_char == 'ε' or first_char.isdigit() or
                                first_char in terminal_b or first_char in terminal_c):
                            firsts[non_terminal].add(first_char)
                        elif first_char in productions:
                            stack.append(first_char)

        completed[non_terminal] = True
        return firsts[non_terminal]

    for non_terminal in productions:
        calculate_first(non_terminal)

    return firsts


def calculate_follow_in(productions, firsts):
    follows = {}
    for non_terminal in productions:
        follows[non_terminal] = set()

    start_symbol = list(productions.keys())[0]
    follows[start_symbol].add('$')

    while True:
        updated = False

        for non_terminal in productions:
            for production in productions[non_terminal]:
                follow_temp = follows[non_terminal].copy()
                for symbol in reversed(production):
                    if symbol in productions:
                        if follows[symbol].union(follow_temp) != follows[symbol]:
                            follows[symbol].update(follow_temp)
                            updated = True

                        if 'ε' in firsts[symbol]:
                            follow_temp.update(firsts[symbol] - {'ε'})
                        else:
                            follow_temp = firsts[symbol].copy()
                    else:
                        follow_temp = {symbol}

        if not updated:
            break

    return follows


def calculate_select_in(productions, firsts, follows):
    selects = {}

    for non_terminal in productions:
        for production in productions[non_terminal]:
            select_key = f"{non_terminal} -> {production}"
            if select_key not in selects:
                selects[select_key] = set()

            first_set = set()
            if production:
                if production[0:3] in terminal_e:
                    first_set.add(production[0:3])
                else:
                    for char in production:
                        if char in terminal_b or char in terminal_c or char.islower() or char.isdigit():
                            first_set.add(char)
                            break
                        elif char in productions:
                            first_set.update(firsts[char])
                            if 'ε' not in firsts[char]:
                                break
                    else:
                        if 'ε' in firsts.get(production[-1], set()):
                            first_set.add('ε')

            if 'ε' in first_set:
                first_set.remove('ε')
                first_set.update(follows[non_terminal])  # 更新为添加FOLLOW集合中的元素

            selects[select_key].update(first_set)

    return selects


def is_ll1(selects):
    # 创建一个字典，用于记录每个非终结符对应的选择集
    non_terminal_selects = {}

    # 遍历所有产生式的选择集
    for key, select_set in selects.items():
        # 提取产生式左部非终结符
        non_terminal = key.split('->')[0].strip()

        # 如果该非终结符不在选择集字典中，则将其添加进去
        if non_terminal not in non_terminal_selects:
            non_terminal_selects[non_terminal] = []

        # 记录产生式左部非终结符、产生式右部和选择集
        non_terminal_selects[non_terminal].append((non_terminal, key.split('->')[1].strip(), select_set))

    # 创建一个列表，用于记录冲突的产生式
    conflict_productions = []

    # 遍历所有非终结符的产生式选择集
    for non_terminal, productions in non_terminal_selects.items():
        # 遍历该非终结符的所有产生式
        for i in range(len(productions)):
            # 获取当前产生式的选择集
            current_production = productions[i]

            # 遍历当前产生式后面的所有产生式，与当前产生式进行比较
            for j in range(i + 1, len(productions)):
                # 获取后面产生式的选择集
                next_production = productions[j]

                # 如果两个产生式的选择集有交集，则记录冲突的产生式
                if set(current_production[2]).intersection(set(next_production[2])):
                    conflict_productions.append((current_production, next_production))
    if conflict_productions:
        return conflict_productions
    else:
        return []


if __name__ == "__main__":
    terminal_b = ['+', '-', '*', '/', '^', '%', '&', '=', '!']
    terminal_c = ['[', ']', '{', '}', '(', ')', ',', '.', '\\', '"', '\'', '#', '@']
    terminal_e = ['id', 'if']
    create_window()
