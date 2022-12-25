# Where should we write the GIF?
Output demo.gif

Set Shell zsh
Set Theme {"name":"nord","black":"#3b4252","red":"#bf616a","green":"#a3be8c","yellow":"#ebcb8b","blue":"#81a1c1","magenta":"#b48ead","cyan":"#88c0d0","white":"#e5e9f0","brightBlack":"#4c566a","brightRed":"#bf616a","brightGreen":"#a3be8c","brightYellow":"#ebcb8b","brightBlue":"#81a1c1","brightMagenta":"#b48ead","brightCyan":"#8fbcbb","brightWhite":"#eceff4","background":"#2e3440","foreground":"#d8dee9"}
Set FontSize 16
Set Width 550
Set Height 320

# Run the animation command

Hide
Sleep 0.1s
Type 'clear && python animation.py < input.txt'
Enter
Sleep 0.05s
Show

# Wait for the animation to finish
Sleep 15s
