from console import Console
console = Console()
console.show("Normal message")
console.show_info("Normal message")
console.show_warning("Warning message")
console.show_success("Success!!!")
console.show_danger("Danger!!!")
for i in range(101):
    console.show_progress(i)


