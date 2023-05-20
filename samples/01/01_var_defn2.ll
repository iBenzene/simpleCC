; ModuleID = 'sysy2022_compiler'
source_filename = "../input/../input/01_var_defn2.sy"

@a = global i32 3
@b = global i32 5
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
  store i32 5, i32* %op0
  %op1 = load i32, i32* %op0
  %op2 = load i32, i32* @b
  %op3 = add i32 %op1, %op2
  ret i32 %op3
}
