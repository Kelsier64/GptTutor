import azure_o1
for steps, total_thinking_time in azure_o1.generate_response("9.8 vs 9.11 which is bigger"):
    if steps[-1][0]=="Final Answer":
        print(steps[-1][1])
