"""
merge_pdf_baoxiao.py

Author: yqxiong
Date: 2024-09-09
"""

import os, sys
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from tkinter import Tk, filedialog, messagebox

# 注册字体
def register_font():
    font_path = "resources/msyh.ttc"
    if hasattr(sys, '_MEIPASS'):
        font_path = os.path.join(getattr(sys, '_MEIPASS'), font_path)
    pdfmetrics.registerFont(TTFont('MicrosoftYaHei', font_path))

# 缩放 PDF 页面至 A4 尺寸
def resize_to_a4(input_pdf, scale_factor=0.9):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    output_pdf = input_pdf + ".temp.pdf"

    # A4 尺寸
    a4_width, a4_height = A4

    for page_num in range(len(reader.pages)):
        original_page = reader.pages[page_num]
        media_box = original_page.mediabox

        # 获取原页面的尺寸
        original_width = float(media_box.width)
        original_height = float(media_box.height)

        # 计算宽度和高度的缩放比例，以适应横板A4
        scale_x = a4_width / original_width
        scale_y = a4_height / original_height
        scale = min(scale_x, scale_y)  # 保证页面内容不被裁剪，选择较小的缩放比例

        # 设置新的页面尺寸为 A4
        original_page.scale_by(scale * scale_factor)  # 按照缩放比例调整页面

        # 更新页面的 media box 以适应 A4
        original_page.mediabox.lower_left = (0, 0)
        original_page.mediabox.upper_right = (a4_width, a4_height)

        # 将页面添加到 writer 中
        writer.add_page(original_page)

    # 写入输出的 PDF 文件
    with open(output_pdf, "wb") as out_f:
        writer.write(out_f)
    
    return output_pdf

# 使用 reportlab 生成带有文件名的 PDF 页面
def create_filename_page(filename, output_path):

    c = canvas.Canvas(output_path, pagesize=A4, initialFontName='MicrosoftYaHei')

    # 在页面上插入文件名，位置是 (x=100, y=100)，可以根据需要调整
    c.drawString(100, 100, f"{os.path.basename(filename).strip(".pdf.temp.pdf")}")

    # 设置中文字体
    c.setFont("MicrosoftYaHei", 18);
    
    # 保存 PDF
    c.showPage()
    c.save()

# 合并 PDF 文件，并在每一页后面添加文件名
def merge_pdfs(pdf_files, output_file):
    writer = PdfWriter()

    for file_idx, file in enumerate(pdf_files):
        reader = PdfReader(file)
        num_pages = len(reader.pages)

        for i in range(num_pages):
            # 添加文件内容
            writer.add_page(reader.pages[i])
        
        # 在文件后添加文件名页
        filename_page = f"temp_filename_page_{file_idx}.pdf"
        create_filename_page(file, filename_page)
        
        # 读取生成的文件名页
        with open(filename_page, "rb") as f:
            name_reader = PdfReader(f)
            writer.add_page(name_reader.pages[0])

        # 删除临时文件
        os.remove(filename_page)

    # 写入合并文件
    with open(output_file, "wb") as output_pdf:
        writer.write(output_pdf)

# 选择 PDF 文件
def select_files():
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    file_paths = filedialog.askopenfilenames(
        title="选择要合并的PDF文件",
        filetypes=[("PDF files", "*.pdf")]
    )
    return list(file_paths)

# 主程序入口
if __name__ == "__main__":
    # 注册字体
    register_font()

    # 让用户选择要合并的PDF文件
    pdf_files = select_files()

    if not pdf_files:
        messagebox.showerror("未选择", "请选择至少一个PDF文件")
    else:
        # 调整pdf比例
        scaled_pdfs = []
        for pdf_file in pdf_files:
            scaled_pdfs.append(resize_to_a4(pdf_file, 0.9))
        

        # 设置输出文件的路径
        output_file = filedialog.asksaveasfilename(
            title="保存合并后的PDF文件",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="合并后.pdf"
        )

        if output_file:
            # 合并 PDF 文件并在偶数页添加文件名
            merge_pdfs(scaled_pdfs, output_file)

            # 显示完成信息
            messagebox.showinfo("成功", f"合并后的PDF位于 {output_file}")
        else:
            messagebox.showerror("未操作", "没有选择输出路径")
        
        # 删除临时生成的调整比例后的 PDF 文件
        for scaled_pdf in scaled_pdfs:
            os.remove(scaled_pdf)
        
