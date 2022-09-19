const problems = ["AAABBDD", "ABCABC", "DDBBAA"];
function solution(problems) {
  let answer = 0;

  for (let i = 0; i < problems.length; i++) {
    let ref = problems[i].split("").sort().join("");

    if (problems[i] === ref) answer++;
  }

  return answer;
}
console.log(answer);
