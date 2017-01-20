import sentenceAlign as sa

ch='在微妙的國際形勢之中，我們的經濟保持穩定的運行，克服了諸多困難。'
po=' Apesar da delicada conjuntura internacional, nossa economia continua firme e superando desafios. Acabamos de dar uma prova contundente.'

r=sa.parallel(ch,po,1.1,3.5)
print(r[0])
print(r[1])