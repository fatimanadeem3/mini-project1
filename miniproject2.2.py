def fizzbuss(n):
    last_num_sum =0
    for i in range(1,n+1):
        present_num=last_num_sum +i
        last_num_sum=present_num
        if present_num % 7 == 0 and present_num % 9 == 0:
            print(f"---Fizz-Buzz---:{present_num}")
                
        elif present_num % 7 == 0:
            print(f"---Fizz---:{present_num}:fizz")
        elif present_num % 9 == 0:
            print(f"---Buzz---:{present_num}:buzz")
        else:
            print(present_num)
             


fizzbuss(50)