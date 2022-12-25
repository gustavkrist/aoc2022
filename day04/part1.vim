let lines = getline(1, '$')
let part1 = 0
let part2 = 0
for line in lines
  let elves = split(line, ',')
  let elf1 = map(split(elves[0], '-'), 'str2nr(v:val)')
  let elf2 = map(split(elves[1], '-'), 'str2nr(v:val)')
  let part1 += (elf1[0] <= elf2[0] && elf1[1] >= elf2[1]) || (elf1[0] >= elf2[0] && elf1[1] <= elf2[1])
  let part2 += elf1[0] <= elf2[1] && elf2[0] <= elf1[1]
endfor
echo(part1)
echo(part2)
