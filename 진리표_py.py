def dec2b(bit, num):
    binary = ""

    while bit != 0:
        value = num % 2
        if value == 0 or num == 0:
            binary = "0"+binary
        else:
            binary = "1"+binary
        num = num//2
        bit -= 1

    return binary

    
def print_truth(para, combine):
    n = len(para)
    bit = {}

    # parameter 변수로 할당
    for i in para:
        bit[i] = 0
        print(i, end=' ')

    print('| out')

    i = 0
    while i < len(combine):
        if combine[i] in para:
            combine = combine[:i] + f'bit["{combine[i]}"]' + combine[i+1:]
            i += 8
        else:
            i += 1

    for i in range(2**n):
        binary = dec2b(n, i)
        for j in range(n):
            bit[para[j]] = int(binary[j])
            
        for j in para:
            print(bit[j], end=' ')
            
        result = eval(combine, {'bit': bit})
        print(f'| {result}')

    return


while True:
    para = input("""파라미터 입력 (공백 구분, 끝내려면 n)\n: """).split()
    if para == ['n']:
        print("종료")
        break
    combine = input("""식 입력 (and: &, or: |, not: ~, xor: ^)\n: """)

    print_truth(para, combine)
    print()
        
