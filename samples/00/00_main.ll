; ModuleID = 'sysy2022_compiler'
source_filename = "../input/../input/00_main.sy"

declare i32 @getint()

declare i32 @getch()

declare i32 @getarray(i32*)

declare void @putint(i32)

declare void @putch(i32)

declare void @putarray(i32, i32*)

declare void @starttime()

declare void @stoptime()

define void @defn() {
defn_ENTRY:
  ret i32 3
}
