; ModuleID = 'sysy2022_compiler'
source_filename = "../input/../input/02_var_defn3.sy"

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
  %op0 = alloca i32
  %op1 = alloca i32
  %op2 = alloca i32
  %op3 = load i32, i32* %op0
  store i32 %op3, i32 1
  %op4 = load i32, i32* %op1
  store i32 %op4, i32 2
  %op5 = load i32, i32* %op2
  store i32 %op5, i32 3
  %op6 = load i32, i32* %op1
  %op7 = load i32, i32* %op2
  %op8 = add i32 %op6, %op7
  ret i32 %op8
}
