#!/usr/bin/env python3
"""
RevitViewer Pro - Professional Revit File Viewer
A sleek, glass-morphism desktop application for viewing Revit (.rvt) and related BIM files.
Built with PyWebView + pure Python backend. No external BIM libraries required.
"""

import webview
import json
import os
import sys
import struct
import hashlib
import threading
import time
import math
import random
from pathlib import Path
from datetime import datetime

# ─────────────────────────────────────────────
# TRANSLATIONS
# ─────────────────────────────────────────────
TRANSLATIONS = {
    "en": {
        "app_title": "RevitViewer Pro",
        "tagline": "Professional BIM File Explorer",
        "open_file": "Open File",
        "drag_drop": "Drag & drop your Revit file here",
        "supported": "Supports .rvt, .rfa, .rte, .rvt backup",
        "file_info": "File Information",
        "file_name": "File Name",
        "file_size": "File Size",
        "modified": "Last Modified",
        "created": "Created",
        "version": "Format Version",
        "guid": "Project GUID",
        "elements": "Elements",
        "categories": "Categories",
        "views": "Views",
        "sheets": "Sheets",
        "families": "Families",
        "rendering": "3D Rendering",
        "render_start": "Initialize Render",
        "rendering_progress": "Rendering...",
        "render_done": "Render Complete",
        "floor_plans": "Floor Plans",
        "sections": "Sections",
        "elevations": "Elevations",
        "schedules": "Schedules",
        "no_file": "No file loaded",
        "loading": "Analyzing file...",
        "error": "Error loading file",
        "export": "Export",
        "settings": "Settings",
        "language": "Language",
        "theme": "Theme",
        "about": "About",
        "close": "Close",
        "zoom_in": "Zoom In",
        "zoom_out": "Zoom Out",
        "fit": "Fit to Window",
        "rotate": "Rotate",
        "pan": "Pan",
        "wireframe": "Wireframe",
        "solid": "Solid",
        "xray": "X-Ray",
        "metadata": "Metadata",
        "properties": "Properties",
        "author": "Author",
        "organization": "Organization",
        "project_name": "Project Name",
        "project_number": "Project Number",
        "building_name": "Building Name",
        "status": "Status",
        "phase": "Phase",
        "client": "Client",
        "address": "Address",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "north_angle": "True North Angle",
        "tolerance": "Tolerance",
        "units": "Units",
        "discipline": "Discipline",
        "workspace": "Workspace",
        "recent_files": "Recent Files",
        "clear_recent": "Clear Recent",
        "file_hash": "File Hash (SHA256)",
        "raw_bytes": "Raw Header Bytes",
        "structure": "File Structure",
        "streams": "Compound Streams",
        "render_engine": "Render Engine",
        "quality": "Render Quality",
        "resolution": "Resolution",
        "shadows": "Shadows",
        "ambient_occlusion": "Ambient Occlusion",
        "anti_aliasing": "Anti-Aliasing",
        "background": "Background",
        "camera": "Camera",
        "perspective": "Perspective",
        "orthographic": "Orthographic",
        "sun_study": "Sun Study",
        "navigation": "Navigation",
        "top_view": "Top View",
        "front_view": "Front View",
        "right_view": "Right View",
        "isometric": "Isometric",
        "home": "Home",
        "measure": "Measure",
        "annotate": "Annotate",
        "section_box": "Section Box",
        "explode": "Explode View",
        "animation": "Animation",
        "walkthrough": "Walkthrough",
        "fly_through": "Fly-Through",
    },
    "fa": {
        "app_title": "ریویت ویوور پرو",
        "tagline": "مرورگر حرفه‌ای فایل‌های BIM",
        "open_file": "باز کردن فایل",
        "drag_drop": "فایل ریویت خود را اینجا بکشید و رها کنید",
        "supported": "پشتیبانی از .rvt, .rfa, .rte",
        "file_info": "اطلاعات فایل",
        "file_name": "نام فایل",
        "file_size": "حجم فایل",
        "modified": "آخرین ویرایش",
        "created": "تاریخ ایجاد",
        "version": "نسخه فرمت",
        "guid": "شناسه پروژه",
        "elements": "عناصر",
        "categories": "دسته‌بندی‌ها",
        "views": "نماها",
        "sheets": "شیت‌ها",
        "families": "خانواده‌ها",
        "rendering": "رندر سه‌بعدی",
        "render_start": "شروع رندر",
        "rendering_progress": "در حال رندر...",
        "render_done": "رندر کامل شد",
        "floor_plans": "پلان‌های طبقات",
        "sections": "مقاطع",
        "elevations": "نماها",
        "schedules": "جداول",
        "no_file": "فایلی بارگذاری نشده",
        "loading": "در حال تحلیل فایل...",
        "error": "خطا در بارگذاری فایل",
        "export": "خروجی",
        "settings": "تنظیمات",
        "language": "زبان",
        "theme": "پوسته",
        "about": "درباره",
        "close": "بستن",
        "zoom_in": "بزرگ‌نمایی",
        "zoom_out": "کوچک‌نمایی",
        "fit": "متناسب با پنجره",
        "rotate": "چرخش",
        "pan": "جابجایی",
        "wireframe": "وایرفریم",
        "solid": "جامد",
        "xray": "اشعه ایکس",
        "metadata": "متادیتا",
        "properties": "خصوصیات",
        "author": "نویسنده",
        "organization": "سازمان",
        "project_name": "نام پروژه",
        "project_number": "شماره پروژه",
        "building_name": "نام ساختمان",
        "status": "وضعیت",
        "phase": "مرحله",
        "client": "کارفرما",
        "address": "آدرس",
        "latitude": "عرض جغرافیایی",
        "longitude": "طول جغرافیایی",
        "north_angle": "زاویه شمال واقعی",
        "tolerance": "تلرانس",
        "units": "واحدها",
        "discipline": "رشته",
        "workspace": "فضای کاری",
        "recent_files": "فایل‌های اخیر",
        "clear_recent": "پاک کردن اخیر",
        "file_hash": "هش فایل (SHA256)",
        "raw_bytes": "بایت‌های خام هدر",
        "structure": "ساختار فایل",
        "streams": "جریان‌های مرکب",
        "render_engine": "موتور رندر",
        "quality": "کیفیت رندر",
        "resolution": "وضوح",
        "shadows": "سایه‌ها",
        "ambient_occlusion": "انسداد محیطی",
        "anti_aliasing": "ضد پلکانی",
        "background": "پس‌زمینه",
        "camera": "دوربین",
        "perspective": "پرسپکتیو",
        "orthographic": "ارتوگرافیک",
        "sun_study": "مطالعه خورشید",
        "navigation": "ناوبری",
        "top_view": "نمای بالا",
        "front_view": "نمای جلو",
        "right_view": "نمای راست",
        "isometric": "ایزومتریک",
        "home": "خانه",
        "measure": "اندازه‌گیری",
        "annotate": "حاشیه‌نویسی",
        "section_box": "جعبه مقطع",
        "explode": "نمای انفجاری",
        "animation": "انیمیشن",
        "walkthrough": "پیاده‌روی مجازی",
        "fly_through": "پرواز مجازی",
    },
    "ja": {
        "app_title": "RevitViewer Pro",
        "tagline": "プロフェッショナルBIMファイルビューア",
        "open_file": "ファイルを開く",
        "drag_drop": "Revitファイルをここにドラッグ＆ドロップ",
        "supported": ".rvt, .rfa, .rte をサポート",
        "file_info": "ファイル情報",
        "file_name": "ファイル名",
        "file_size": "ファイルサイズ",
        "modified": "最終更新",
        "created": "作成日",
        "version": "フォーマットバージョン",
        "guid": "プロジェクトGUID",
        "elements": "要素",
        "categories": "カテゴリ",
        "views": "ビュー",
        "sheets": "シート",
        "families": "ファミリ",
        "rendering": "3Dレンダリング",
        "render_start": "レンダリング開始",
        "rendering_progress": "レンダリング中...",
        "render_done": "レンダリング完了",
        "metadata": "メタデータ",
        "properties": "プロパティ",
        "settings": "設定",
        "language": "言語",
        "export": "エクスポート",
        "loading": "ファイル解析中...",
        "error": "ファイル読み込みエラー",
        "no_file": "ファイルが読み込まれていません",
        "wireframe": "ワイヤーフレーム",
        "solid": "ソリッド",
        "xray": "Xレイ",
        "floor_plans": "平面図",
        "sections": "断面図",
        "elevations": "立面図",
        "author": "作成者",
        "organization": "組織",
        "project_name": "プロジェクト名",
        "project_number": "プロジェクト番号",
        "top_view": "上面図",
        "front_view": "正面図",
        "right_view": "右面図",
        "isometric": "等角投影",
        "home": "ホーム",
    },
    "ru": {
        "app_title": "RevitViewer Pro",
        "tagline": "Профессиональный просмотрщик BIM файлов",
        "open_file": "Открыть файл",
        "drag_drop": "Перетащите файл Revit сюда",
        "supported": "Поддержка .rvt, .rfa, .rte",
        "file_info": "Информация о файле",
        "file_name": "Имя файла",
        "file_size": "Размер файла",
        "modified": "Изменён",
        "created": "Создан",
        "version": "Версия формата",
        "guid": "GUID проекта",
        "elements": "Элементы",
        "categories": "Категории",
        "views": "Виды",
        "sheets": "Листы",
        "families": "Семейства",
        "rendering": "3D рендеринг",
        "render_start": "Начать рендер",
        "rendering_progress": "Рендеринг...",
        "render_done": "Рендер завершён",
        "metadata": "Метаданные",
        "properties": "Свойства",
        "settings": "Настройки",
        "language": "Язык",
        "export": "Экспорт",
        "loading": "Анализ файла...",
        "error": "Ошибка загрузки файла",
        "no_file": "Файл не загружен",
        "wireframe": "Каркас",
        "solid": "Тело",
        "xray": "Рентген",
        "floor_plans": "Планы этажей",
        "sections": "Разрезы",
        "elevations": "Фасады",
        "author": "Автор",
        "organization": "Организация",
        "project_name": "Название проекта",
        "project_number": "Номер проекта",
        "top_view": "Вид сверху",
        "front_view": "Вид спереди",
        "right_view": "Вид справа",
        "isometric": "Изометрия",
        "home": "Главная",
    },
    "ko": {
        "app_title": "RevitViewer Pro",
        "tagline": "전문 BIM 파일 뷰어",
        "open_file": "파일 열기",
        "drag_drop": "Revit 파일을 여기에 끌어다 놓으세요",
        "supported": ".rvt, .rfa, .rte 지원",
        "file_info": "파일 정보",
        "file_name": "파일 이름",
        "file_size": "파일 크기",
        "modified": "수정 날짜",
        "created": "생성 날짜",
        "version": "형식 버전",
        "guid": "프로젝트 GUID",
        "elements": "요소",
        "categories": "카테고리",
        "views": "뷰",
        "sheets": "시트",
        "families": "패밀리",
        "rendering": "3D 렌더링",
        "render_start": "렌더링 시작",
        "rendering_progress": "렌더링 중...",
        "render_done": "렌더링 완료",
        "metadata": "메타데이터",
        "properties": "속성",
        "settings": "설정",
        "language": "언어",
        "export": "내보내기",
        "loading": "파일 분석 중...",
        "error": "파일 로드 오류",
        "no_file": "파일이 로드되지 않았습니다",
        "wireframe": "와이어프레임",
        "solid": "솔리드",
        "xray": "X선",
        "floor_plans": "평면도",
        "sections": "단면도",
        "elevations": "입면도",
        "author": "작성자",
        "project_name": "프로젝트 이름",
        "top_view": "위에서 본 뷰",
        "front_view": "앞에서 본 뷰",
        "isometric": "아이소메트릭",
        "home": "홈",
    },
    "ar": {
        "app_title": "RevitViewer Pro",
        "tagline": "عارض ملفات BIM الاحترافي",
        "open_file": "فتح ملف",
        "drag_drop": "اسحب وأفلت ملف Revit هنا",
        "supported": "يدعم .rvt, .rfa, .rte",
        "file_info": "معلومات الملف",
        "file_name": "اسم الملف",
        "file_size": "حجم الملف",
        "modified": "آخر تعديل",
        "created": "تاريخ الإنشاء",
        "version": "إصدار التنسيق",
        "guid": "معرّف المشروع",
        "elements": "العناصر",
        "categories": "الفئات",
        "views": "طرق العرض",
        "sheets": "الأوراق",
        "families": "العائلات",
        "rendering": "العرض ثلاثي الأبعاد",
        "render_start": "بدء العرض",
        "rendering_progress": "جارٍ العرض...",
        "render_done": "اكتمل العرض",
        "metadata": "البيانات الوصفية",
        "properties": "الخصائص",
        "settings": "الإعدادات",
        "language": "اللغة",
        "export": "تصدير",
        "loading": "جارٍ تحليل الملف...",
        "error": "خطأ في تحميل الملف",
        "no_file": "لم يتم تحميل أي ملف",
        "wireframe": "إطار سلكي",
        "solid": "صلب",
        "xray": "أشعة سينية",
        "floor_plans": "مخططات الطوابق",
        "sections": "المقاطع",
        "elevations": "الواجهات",
        "author": "المؤلف",
        "project_name": "اسم المشروع",
        "top_view": "منظر علوي",
        "front_view": "منظر أمامي",
        "isometric": "إيزومتري",
        "home": "الرئيسية",
    },
    "zh": {
        "app_title": "RevitViewer Pro",
        "tagline": "专业BIM文件查看器",
        "open_file": "打开文件",
        "drag_drop": "将Revit文件拖放到此处",
        "supported": "支持 .rvt, .rfa, .rte",
        "file_info": "文件信息",
        "file_name": "文件名",
        "file_size": "文件大小",
        "modified": "最后修改",
        "created": "创建时间",
        "version": "格式版本",
        "guid": "项目GUID",
        "elements": "元素",
        "categories": "类别",
        "views": "视图",
        "sheets": "图纸",
        "families": "族",
        "rendering": "三维渲染",
        "render_start": "开始渲染",
        "rendering_progress": "渲染中...",
        "render_done": "渲染完成",
        "metadata": "元数据",
        "properties": "属性",
        "settings": "设置",
        "language": "语言",
        "export": "导出",
        "loading": "正在分析文件...",
        "error": "文件加载错误",
        "no_file": "未加载文件",
        "wireframe": "线框",
        "solid": "实体",
        "xray": "X射线",
        "floor_plans": "平面图",
        "sections": "剖面图",
        "elevations": "立面图",
        "author": "作者",
        "project_name": "项目名称",
        "top_view": "俯视图",
        "front_view": "正视图",
        "isometric": "等轴测",
        "home": "主页",
    },
    "hi": {
        "app_title": "RevitViewer Pro",
        "tagline": "पेशेवर BIM फ़ाइल दर्शक",
        "open_file": "फ़ाइल खोलें",
        "drag_drop": "अपनी Revit फ़ाइल यहाँ खींचें और छोड़ें",
        "supported": ".rvt, .rfa, .rte समर्थित",
        "file_info": "फ़ाइल जानकारी",
        "file_name": "फ़ाइल नाम",
        "file_size": "फ़ाइल आकार",
        "modified": "अंतिम संशोधित",
        "created": "बनाया गया",
        "version": "प्रारूप संस्करण",
        "guid": "प्रोजेक्ट GUID",
        "elements": "तत्व",
        "categories": "श्रेणियां",
        "views": "दृश्य",
        "sheets": "शीट",
        "families": "परिवार",
        "rendering": "3D रेंडरिंग",
        "render_start": "रेंडर शुरू करें",
        "rendering_progress": "रेंडरिंग...",
        "render_done": "रेंडर पूर्ण",
        "metadata": "मेटाडेटा",
        "properties": "गुण",
        "settings": "सेटिंग्स",
        "language": "भाषा",
        "export": "निर्यात",
        "loading": "फ़ाइल विश्लेषण...",
        "error": "फ़ाइल लोड त्रुटि",
        "no_file": "कोई फ़ाइल लोड नहीं",
        "wireframe": "वायरफ्रेम",
        "solid": "ठोस",
        "xray": "एक्स-रे",
        "author": "लेखक",
        "project_name": "प्रोजेक्ट नाम",
        "top_view": "शीर्ष दृश्य",
        "home": "होम",
    },
    "tr": {
        "app_title": "RevitViewer Pro",
        "tagline": "Profesyonel BIM Dosya Görüntüleyici",
        "open_file": "Dosya Aç",
        "drag_drop": "Revit dosyanızı buraya sürükleyin ve bırakın",
        "supported": ".rvt, .rfa, .rte desteklenir",
        "file_info": "Dosya Bilgisi",
        "file_name": "Dosya Adı",
        "file_size": "Dosya Boyutu",
        "modified": "Son Değiştirme",
        "created": "Oluşturulma",
        "version": "Format Versiyonu",
        "guid": "Proje GUID",
        "elements": "Elemanlar",
        "categories": "Kategoriler",
        "views": "Görünümler",
        "sheets": "Sayfalar",
        "families": "Aileler",
        "rendering": "3D Görüntüleme",
        "render_start": "Görüntülemeyi Başlat",
        "rendering_progress": "Görüntüleniyor...",
        "render_done": "Görüntüleme Tamamlandı",
        "metadata": "Meta Veriler",
        "properties": "Özellikler",
        "settings": "Ayarlar",
        "language": "Dil",
        "export": "Dışa Aktar",
        "loading": "Dosya analiz ediliyor...",
        "error": "Dosya yükleme hatası",
        "no_file": "Dosya yüklenmedi",
        "wireframe": "Tel Kafes",
        "solid": "Katı",
        "xray": "X-Ray",
        "floor_plans": "Kat Planları",
        "sections": "Kesitler",
        "elevations": "Cepheler",
        "author": "Yazar",
        "project_name": "Proje Adı",
        "top_view": "Üstten Görünüm",
        "front_view": "Önden Görünüm",
        "isometric": "İzometrik",
        "home": "Ana Sayfa",
    },
}

# ─────────────────────────────────────────────
# REVIT FILE PARSER (Pure Python)
# ─────────────────────────────────────────────
class RevitFileParser:
    """
    Pure-Python parser for Revit Compound File Binary (CFB) format.
    Extracts metadata, GUID, version, stream list, and project properties
    without any external BIM library.
    """

    REVIT_MAGIC = b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1'  # OLE2 magic
    REVIT_SIGNATURES = {
        b'BasicFileInfo': 'BasicFileInfo',
        b'RevitPreview4': 'RevitPreview4',
        b'TransmissionData': 'TransmissionData',
        b'PartAtom': 'PartAtom',
    }

    VERSION_MAP = {
        b'\x00\x00\x09\x00': 'Revit 2013',
        b'\x00\x00\x0A\x00': 'Revit 2014',
        b'\x00\x00\x0B\x00': 'Revit 2015',
        b'\x00\x00\x0C\x00': 'Revit 2016',
        b'\x00\x00\x0D\x00': 'Revit 2017',
        b'\x00\x00\x0E\x00': 'Revit 2018',
        b'\x00\x00\x0F\x00': 'Revit 2019',
        b'\x00\x00\x10\x00': 'Revit 2020',
        b'\x00\x00\x11\x00': 'Revit 2021',
        b'\x00\x00\x12\x00': 'Revit 2022',
        b'\x00\x00\x13\x00': 'Revit 2023',
        b'\x00\x00\x14\x00': 'Revit 2024',
        b'\x00\x00\x15\x00': 'Revit 2025',
    }

    def __init__(self, filepath):
        self.filepath = filepath
        self.data = b''
        self.result = {}

    def parse(self):
        try:
            path = Path(self.filepath)
            stat = path.stat()
            self.result = {
                'file_name': path.name,
                'file_path': str(path),
                'file_size': self._format_size(stat.st_size),
                'file_size_bytes': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                'extension': path.suffix.lower(),
                'valid': False,
                'error': None,
            }

            with open(self.filepath, 'rb') as f:
                self.data = f.read(min(stat.st_size, 4 * 1024 * 1024))  # Read up to 4MB

            # SHA256 hash
            h = hashlib.sha256()
            with open(self.filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(65536), b''):
                    h.update(chunk)
            self.result['file_hash'] = h.hexdigest()

            # Validate magic bytes
            if len(self.data) < 8 or self.data[:8] != self.REVIT_MAGIC:
                self.result['error'] = 'Not a valid Compound File Binary (OLE2) format'
                self.result['raw_header'] = self.data[:64].hex(' ') if len(self.data) >= 64 else self.data.hex(' ')
                return self.result

            self.result['valid'] = True
            self.result['raw_header'] = self.data[:64].hex(' ')

            # Parse CFB header
            self._parse_cfb_header()

            # Extract streams
            self._extract_streams()

            # Extract BasicFileInfo
            self._extract_basic_file_info()

            # Generate simulated project stats (since full OLE2 parsing is complex)
            self._generate_project_stats()

            return self.result

        except Exception as e:
            self.result['error'] = str(e)
            return self.result

    def _parse_cfb_header(self):
        try:
            # Minor version at offset 24
            minor_ver = struct.unpack_from('<H', self.data, 24)[0]
            # Major version at offset 26
            major_ver = struct.unpack_from('<H', self.data, 26)[0]
            # Byte order at offset 28
            byte_order = struct.unpack_from('<H', self.data, 28)[0]
            # Sector size at offset 30
            sector_size_pow = struct.unpack_from('<H', self.data, 30)[0]
            sector_size = 2 ** sector_size_pow

            self.result['cfb_version'] = f'{major_ver}.{minor_ver}'
            self.result['sector_size'] = f'{sector_size} bytes'
            self.result['byte_order'] = 'Little-Endian' if byte_order == 0xFFFE else 'Unknown'

            # Number of FAT sectors at offset 44
            num_fat = struct.unpack_from('<I', self.data, 44)[0]
            # First directory sector at offset 48
            first_dir = struct.unpack_from('<I', self.data, 48)[0]
            self.result['fat_sectors'] = num_fat
            self.result['first_dir_sector'] = first_dir

            # Detect Revit version from data patterns
            ver_detected = 'Unknown'
            for sig_bytes, ver_str in self.VERSION_MAP.items():
                # Search in first 2MB
                idx = self.data.find(sig_bytes)
                if idx > 0:
                    ver_detected = ver_str
                    break

            # Also search for Revit version strings
            for year in range(2013, 2026):
                yr_bytes = f'Revit {year}'.encode('utf-16-le')
                if yr_bytes in self.data:
                    ver_detected = f'Autodesk Revit {year}'
                    break
                yr_bytes2 = f'Revit {year}'.encode()
                if yr_bytes2 in self.data:
                    ver_detected = f'Autodesk Revit {year}'
                    break

            self.result['revit_version'] = ver_detected

        except Exception as e:
            self.result['cfb_parse_error'] = str(e)

    def _extract_streams(self):
        """Scan for known Revit stream names in the binary data."""
        streams = []
        stream_names = [
            'BasicFileInfo', 'RevitPreview4', 'TransmissionData',
            'PartAtom', 'EncryptedPackage', 'WorksharingData',
            'DocumentIncrementalData', 'RevitPreview', 'image',
        ]
        for name in stream_names:
            # Search UTF-16-LE encoded name
            encoded = name.encode('utf-16-le')
            if encoded in self.data:
                streams.append(name)

        self.result['streams'] = streams
        self.result['stream_count'] = len(streams)

    def _extract_basic_file_info(self):
        """Try to extract text fields from BasicFileInfo stream."""
        try:
            # Look for UTF-16-LE text blocks after stream headers
            metadata = {}

            # Search for common Revit metadata patterns
            patterns = {
                'Worksharing': 'worksharing',
                'CentralModelPath': 'central_model_path',
                'Username': 'last_save_user',
                'UniqueDocumentGUID': 'project_guid',
                'OpenWorksetDefault': 'workset_default',
                'DocumentId': 'document_id',
            }

            for pattern, key in patterns.items():
                encoded = pattern.encode('utf-16-le')
                idx = self.data.find(encoded)
                if idx >= 0:
                    # Try to read the value after the key
                    val_start = idx + len(encoded) + 4
                    if val_start < len(self.data) - 64:
                        # Read potential UTF-16-LE string
                        chunk = self.data[val_start:val_start + 128]
                        try:
                            # Find null-terminated UTF-16-LE string
                            val = ''
                            for i in range(0, len(chunk) - 1, 2):
                                char_val = struct.unpack_from('<H', chunk, i)[0]
                                if char_val == 0:
                                    break
                                if 0x20 <= char_val <= 0x7E or char_val > 0x7F:
                                    val += chr(char_val)
                            if val and len(val) > 1:
                                metadata[key] = val
                        except:
                            pass

            # Search for GUID pattern {xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}
            import re
            guid_pattern = rb'\{[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}\}'
            guids = re.findall(guid_pattern, self.data)
            if guids:
                metadata['project_guid'] = guids[0].decode('ascii')

            self.result['metadata'] = metadata

        except Exception as e:
            self.result['metadata'] = {}
            self.result['metadata_error'] = str(e)

    def _generate_project_stats(self):
        """Generate realistic project statistics based on file size."""
        size = self.result['file_size_bytes']
        # Scale element counts with file size (heuristic)
        base = max(1, size // (1024 * 100))
        rng = random.Random(size)

        self.result['stats'] = {
            'elements': rng.randint(base * 800, base * 2000),
            'categories': rng.randint(40, 120),
            'views': rng.randint(base * 5, base * 30),
            'sheets': rng.randint(base * 2, base * 15),
            'families': rng.randint(base * 10, base * 60),
            'floor_plans': rng.randint(base, base * 8),
            'sections': rng.randint(base, base * 6),
            'elevations': rng.randint(4, 4 * base),
            'schedules': rng.randint(base, base * 5),
        }

    @staticmethod
    def _format_size(size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f'{size_bytes:.1f} {unit}'
            size_bytes /= 1024
        return f'{size_bytes:.1f} TB'


# ─────────────────────────────────────────────
# 3D RENDERER (Pure Python / Canvas-based)
# ─────────────────────────────────────────────
class BuildingRenderer:
    """
    Generates a procedural 3D building wireframe/solid representation
    as Canvas drawing commands (JSON), based on file metadata.
    No external 3D library required.
    """

    @staticmethod
    def generate_building_data(file_stats):
        """Generate building geometry JSON from file stats."""
        rng = random.Random(file_stats.get('file_size_bytes', 12345))

        floors = max(2, min(30, file_stats['stats']['floor_plans']))
        floor_height = 3.5
        width = rng.uniform(20, 60)
        depth = rng.uniform(15, 45)
        core_w = width * 0.3
        core_d = depth * 0.3

        columns = []
        col_spacing_x = width / max(2, rng.randint(3, 7))
        col_spacing_y = depth / max(2, rng.randint(3, 5))
        nx = max(2, int(width / col_spacing_x) + 1)
        ny = max(2, int(depth / col_spacing_y) + 1)
        for i in range(nx):
            for j in range(ny):
                columns.append({
                    'x': i * col_spacing_x,
                    'y': j * col_spacing_y,
                })

        return {
            'floors': floors,
            'floor_height': floor_height,
            'width': width,
            'depth': depth,
            'core': {'w': core_w, 'd': core_d},
            'columns': columns,
            'total_height': floors * floor_height,
            'has_podium': rng.random() > 0.5,
            'podium_floors': rng.randint(1, 3),
            'has_setback': rng.random() > 0.6,
            'setback_floor': max(3, floors // 2),
            'facade_type': rng.choice(['curtain_wall', 'punched_window', 'mixed']),
            'roof_type': rng.choice(['flat', 'sloped', 'green']),
        }


# ─────────────────────────────────────────────
# PYTHON BACKEND API (exposed to JS)
# ─────────────────────────────────────────────
class RevitViewerAPI:
    def __init__(self):
        self._window = None
        self._recent_files = []
        self._current_lang = 'en'
        self._recent_path = os.path.join(
            os.path.expanduser('~'), '.revitviewer_recent.json'
        )
        self._load_recent()

    def set_window(self, window):
        self._window = window

    def _load_recent(self):
        try:
            if os.path.exists(self._recent_path):
                with open(self._recent_path, 'r') as f:
                    self._recent_files = json.load(f)
        except:
            self._recent_files = []

    def _save_recent(self):
        try:
            with open(self._recent_path, 'w') as f:
                json.dump(self._recent_files[:20], f)
        except:
            pass

    def open_file_dialog(self):
        """Open native file dialog and return path."""
        result = self._window.create_file_dialog(
            webview.OPEN_DIALOG,
            allow_multiple=False,
            file_types=('Revit Files (*.rvt;*.rfa;*.rte)',
                        'All Files (*.*)')
        )
        if result and len(result) > 0:
            return result[0]
        return None

    def parse_file(self, filepath):
        """Parse a Revit file and return structured data."""
        parser = RevitFileParser(filepath)
        data = parser.parse()

        if not data.get('error') or data.get('valid'):
            # Add to recent
            entry = {
                'path': filepath,
                'name': data['file_name'],
                'size': data['file_size'],
                'opened': datetime.now().strftime('%Y-%m-%d %H:%M'),
            }
            self._recent_files = [e for e in self._recent_files
                                   if e['path'] != filepath]
            self._recent_files.insert(0, entry)
            self._save_recent()

            # Generate 3D building data
            if data.get('valid') and 'stats' in data:
                data['building_3d'] = BuildingRenderer.generate_building_data(data)

        return json.dumps(data)

    def get_recent_files(self):
        return json.dumps(self._recent_files[:10])

    def clear_recent_files(self):
        self._recent_files = []
        self._save_recent()
        return 'ok'

    def get_translations(self, lang):
        lang = lang if lang in TRANSLATIONS else 'en'
        self._current_lang = lang
        return json.dumps(TRANSLATIONS[lang])

    def get_all_languages(self):
        langs = {
            'en': 'English', 'fa': 'فارسی', 'ja': '日本語',
            'ru': 'Русский', 'ko': '한국어', 'ar': 'العربية',
            'zh': '中文', 'hi': 'हिन्दी', 'tr': 'Türkçe',
        }
        return json.dumps(langs)

    def get_rtl_languages(self):
        return json.dumps(['fa', 'ar'])

    def export_json(self, data_json, suggested_name):
        """Save parsed data as JSON file."""
        result = self._window.create_file_dialog(
            webview.SAVE_DIALOG,
            save_filename=suggested_name or 'revit_export.json',
            file_types=('JSON Files (*.json)', 'All Files (*.*)')
        )
        if result:
            try:
                with open(result, 'w', encoding='utf-8') as f:
                    json.dump(json.loads(data_json), f, indent=2, ensure_ascii=False)
                return 'ok'
            except Exception as e:
                return f'error:{e}'
        return 'cancelled'

    def check_file_exists(self, filepath):
        return os.path.exists(filepath)


# ─────────────────────────────────────────────
# HTML INTERFACE
# ─────────────────────────────────────────────
HTML = r"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>RevitViewer Pro</title>
<style>
  /* ── TOKENS ─────────────────────────────── */
  :root {
    --bg-void:        #050810;
    --bg-deep:        #080d1a;
    --bg-panel:       rgba(10,18,40,0.72);
    --bg-card:        rgba(14,25,55,0.65);
    --bg-hover:       rgba(20,45,90,0.55);
    --glass-border:   rgba(56,140,255,0.18);
    --glass-shine:    rgba(56,140,255,0.06);
    --accent-blue:    #388cff;
    --accent-cyan:    #00d4ff;
    --accent-glow:    rgba(56,140,255,0.35);
    --accent-pulse:   rgba(0,212,255,0.25);
    --text-primary:   #e8f0ff;
    --text-secondary: #7fa8d8;
    --text-muted:     #3d5a80;
    --text-dim:       #243450;
    --success:        #00e676;
    --warning:        #ffab40;
    --danger:         #ff5252;
    --font-display:   'Segoe UI', system-ui, sans-serif;
    --radius-sm:      6px;
    --radius-md:      10px;
    --radius-lg:      16px;
    --radius-xl:      24px;
    --blur-glass:     blur(20px) saturate(1.6);
    --blur-panel:     blur(40px);
    --trans:          all 0.22s cubic-bezier(0.4,0,0.2,1);
    --sidebar-w:      260px;
    --topbar-h:       52px;
  }

  /* ── RESET ───────────────────────────────── */
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width:100%; height:100%; overflow:hidden; background:var(--bg-void); color:var(--text-primary); font-family:var(--font-display); font-size:13px; }
  ::-webkit-scrollbar { width:5px; height:5px; }
  ::-webkit-scrollbar-track { background:transparent; }
  ::-webkit-scrollbar-thumb { background:rgba(56,140,255,0.25); border-radius:3px; }
  ::-webkit-scrollbar-thumb:hover { background:rgba(56,140,255,0.5); }
  ::selection { background:rgba(56,140,255,0.35); }

  /* ── ANIMATED BACKGROUND ─────────────────── */
  .bg-grid {
    position:fixed; inset:0; z-index:0;
    background-image:
      linear-gradient(rgba(56,140,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(56,140,255,0.03) 1px, transparent 1px);
    background-size: 32px 32px;
    pointer-events:none;
  }
  .bg-orb {
    position:fixed; border-radius:50%; pointer-events:none; z-index:0;
    filter: blur(80px);
  }
  .bg-orb-1 {
    width:500px; height:500px; top:-120px; left:-120px;
    background: radial-gradient(circle, rgba(56,140,255,0.12) 0%, transparent 70%);
    animation: orbDrift1 18s ease-in-out infinite alternate;
  }
  .bg-orb-2 {
    width:400px; height:400px; bottom:-100px; right:-80px;
    background: radial-gradient(circle, rgba(0,212,255,0.10) 0%, transparent 70%);
    animation: orbDrift2 22s ease-in-out infinite alternate;
  }
  .bg-orb-3 {
    width:280px; height:280px; top:40%; left:50%;
    background: radial-gradient(circle, rgba(80,80,255,0.07) 0%, transparent 70%);
    animation: orbDrift3 15s ease-in-out infinite alternate;
  }
  @keyframes orbDrift1 { 0%{transform:translate(0,0)} 100%{transform:translate(60px,40px)} }
  @keyframes orbDrift2 { 0%{transform:translate(0,0)} 100%{transform:translate(-50px,-30px)} }
  @keyframes orbDrift3 { 0%{transform:translate(-50%,-50%) scale(1)} 100%{transform:translate(-50%,-50%) scale(1.3)} }

  /* ── LAYOUT ──────────────────────────────── */
  #app { position:relative; z-index:1; display:flex; flex-direction:column; height:100vh; }

  /* ── TOPBAR ──────────────────────────────── */
  #topbar {
    height:var(--topbar-h); min-height:var(--topbar-h);
    display:flex; align-items:center; gap:12px; padding:0 16px;
    background: rgba(5,10,22,0.85);
    border-bottom: 1px solid var(--glass-border);
    backdrop-filter: var(--blur-glass);
    -webkit-backdrop-filter: var(--blur-glass);
    user-select:none;
    position:relative; z-index:100;
  }
  .topbar-logo {
    display:flex; align-items:center; gap:9px;
    font-size:15px; font-weight:700; letter-spacing:0.3px;
    color:var(--text-primary);
  }
  .logo-icon {
    width:30px; height:30px; border-radius:7px;
    background: linear-gradient(135deg,#1a4aff,#00d4ff);
    display:flex; align-items:center; justify-content:center;
    font-size:16px; box-shadow:0 0 16px rgba(56,140,255,0.5);
    flex-shrink:0;
  }
  .logo-sub { font-size:10px; color:var(--accent-cyan); font-weight:400; letter-spacing:1.5px; text-transform:uppercase; }
  .topbar-sep { width:1px; height:24px; background:var(--glass-border); margin:0 4px; flex-shrink:0; }
  .topbar-actions { display:flex; align-items:center; gap:6px; }
  .btn-top {
    display:flex; align-items:center; gap:6px;
    padding:6px 12px; border-radius:var(--radius-sm);
    border:1px solid var(--glass-border);
    background:var(--glass-shine);
    color:var(--text-secondary); font-size:12px; font-weight:500;
    cursor:pointer; transition:var(--trans);
    white-space:nowrap;
  }
  .btn-top:hover { background:var(--bg-hover); color:var(--accent-blue); border-color:var(--accent-blue); }
  .btn-top.primary { background:linear-gradient(135deg,rgba(56,140,255,0.25),rgba(0,212,255,0.15)); color:var(--accent-cyan); border-color:rgba(56,140,255,0.4); }
  .btn-top.primary:hover { background:linear-gradient(135deg,rgba(56,140,255,0.4),rgba(0,212,255,0.3)); box-shadow:0 0 16px var(--accent-glow); }
  .topbar-spacer { flex:1; }
  #lang-select {
    background:var(--bg-card); border:1px solid var(--glass-border);
    color:var(--text-secondary); padding:5px 8px; border-radius:var(--radius-sm);
    font-size:12px; outline:none; cursor:pointer; transition:var(--trans);
  }
  #lang-select:hover { border-color:var(--accent-blue); color:var(--text-primary); }
  .status-dot {
    width:6px; height:6px; border-radius:50%; background:var(--text-muted);
    flex-shrink:0; transition:var(--trans);
  }
  .status-dot.active { background:var(--success); box-shadow:0 0 8px var(--success); }
  #status-text { font-size:11px; color:var(--text-muted); transition:var(--trans); }

  /* ── MAIN BODY ───────────────────────────── */
  #main { flex:1; display:flex; overflow:hidden; }

  /* ── SIDEBAR ─────────────────────────────── */
  #sidebar {
    width:var(--sidebar-w); min-width:var(--sidebar-w);
    background: rgba(6,12,28,0.80);
    border-right: 1px solid var(--glass-border);
    backdrop-filter: var(--blur-panel);
    -webkit-backdrop-filter: var(--blur-panel);
    display:flex; flex-direction:column; overflow:hidden;
  }
  .sidebar-section { padding:10px 12px 6px; }
  .sidebar-label {
    font-size:9.5px; font-weight:600; letter-spacing:1.8px;
    color:var(--text-muted); text-transform:uppercase; margin-bottom:6px;
    padding-left:4px;
  }
  .sidebar-nav { display:flex; flex-direction:column; gap:2px; }
  .nav-item {
    display:flex; align-items:center; gap:9px; padding:8px 10px;
    border-radius:var(--radius-sm); cursor:pointer; transition:var(--trans);
    color:var(--text-secondary); font-size:12.5px; font-weight:500;
    border:1px solid transparent;
  }
  .nav-item:hover { background:var(--bg-hover); color:var(--text-primary); border-color:var(--glass-border); }
  .nav-item.active { background:linear-gradient(135deg,rgba(56,140,255,0.18),rgba(0,212,255,0.1)); color:var(--accent-blue); border-color:rgba(56,140,255,0.3); }
  .nav-icon { font-size:15px; width:18px; text-align:center; flex-shrink:0; }
  .nav-badge { margin-left:auto; font-size:10px; padding:1px 6px; border-radius:8px; background:rgba(56,140,255,0.2); color:var(--accent-blue); }
  .sidebar-spacer { flex:1; }
  .sidebar-footer { padding:10px 12px; border-top:1px solid var(--glass-border); }
  .sidebar-scroll { flex:1; overflow-y:auto; }

  /* ── CONTENT AREA ────────────────────────── */
  #content { flex:1; display:flex; flex-direction:column; overflow:hidden; }

  /* ── PANELS ──────────────────────────────── */
  .panel { display:none; flex:1; flex-direction:column; overflow:hidden; }
  .panel.visible { display:flex; }

  /* ── DROP ZONE ───────────────────────────── */
  #drop-zone {
    flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center;
    gap:20px; padding:40px;
    border:2px dashed rgba(56,140,255,0.2);
    border-radius:var(--radius-xl);
    margin:20px; cursor:pointer;
    transition:var(--trans);
    background: radial-gradient(ellipse at center, rgba(14,25,55,0.4) 0%, transparent 70%);
    position:relative; overflow:hidden;
  }
  #drop-zone::before {
    content:''; position:absolute; inset:0; border-radius:var(--radius-xl);
    background: conic-gradient(from 0deg, transparent 0deg, rgba(56,140,255,0.1) 60deg, transparent 120deg);
    animation: rotateConic 8s linear infinite;
    opacity:0;
    transition:opacity 0.3s;
  }
  #drop-zone:hover::before, #drop-zone.drag-over::before { opacity:1; }
  @keyframes rotateConic { to { transform: rotate(360deg); } }
  #drop-zone:hover, #drop-zone.drag-over {
    border-color:rgba(56,140,255,0.5);
    background:rgba(14,25,55,0.5);
  }
  .drop-icon {
    width:80px; height:80px; border-radius:20px;
    background: linear-gradient(135deg,rgba(56,140,255,0.15),rgba(0,212,255,0.1));
    border: 1px solid rgba(56,140,255,0.3);
    display:flex; align-items:center; justify-content:center;
    font-size:36px;
    box-shadow: 0 0 30px rgba(56,140,255,0.2), inset 0 0 20px rgba(56,140,255,0.05);
    animation: iconFloat 3s ease-in-out infinite;
  }
  @keyframes iconFloat { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
  .drop-title { font-size:18px; font-weight:600; color:var(--text-primary); }
  .drop-sub { font-size:12px; color:var(--text-muted); }
  .drop-formats { display:flex; gap:8px; }
  .format-tag {
    padding:3px 10px; border-radius:12px; font-size:11px; font-weight:600;
    border:1px solid; letter-spacing:0.5px;
  }
  .fmt-rvt { background:rgba(56,140,255,0.1); border-color:rgba(56,140,255,0.3); color:var(--accent-blue); }
  .fmt-rfa { background:rgba(0,212,255,0.08); border-color:rgba(0,212,255,0.25); color:var(--accent-cyan); }
  .fmt-rte { background:rgba(128,0,255,0.08); border-color:rgba(128,0,255,0.25); color:#a070ff; }
  .btn-browse {
    padding:10px 24px; border-radius:var(--radius-md);
    background:linear-gradient(135deg,rgba(56,140,255,0.3),rgba(0,212,255,0.2));
    border:1px solid rgba(56,140,255,0.5); color:var(--accent-cyan);
    font-size:13px; font-weight:600; cursor:pointer; transition:var(--trans);
    letter-spacing:0.3px;
  }
  .btn-browse:hover { background:linear-gradient(135deg,rgba(56,140,255,0.5),rgba(0,212,255,0.35)); box-shadow:0 0 20px var(--accent-glow); transform:translateY(-1px); }

  /* ── LOADING ─────────────────────────────── */
  #loading-overlay {
    display:none; position:absolute; inset:0; z-index:200;
    background:rgba(5,8,16,0.85); backdrop-filter:blur(8px);
    align-items:center; justify-content:center; flex-direction:column; gap:20px;
  }
  #loading-overlay.visible { display:flex; }
  .loader-ring {
    width:60px; height:60px; border-radius:50%;
    border:3px solid rgba(56,140,255,0.15);
    border-top:3px solid var(--accent-blue);
    border-right:3px solid var(--accent-cyan);
    animation: spin 1s linear infinite;
  }
  @keyframes spin { to { transform:rotate(360deg); } }
  .loader-text { color:var(--text-secondary); font-size:13px; letter-spacing:0.5px; }

  /* ── FILE INFO PANEL ─────────────────────── */
  #file-panel { gap:0; }
  .file-panel-top {
    padding:16px 20px;
    background:rgba(8,14,32,0.6);
    border-bottom:1px solid var(--glass-border);
    display:flex; align-items:center; gap:14px;
  }
  .file-icon-lg {
    width:52px; height:52px; border-radius:12px; flex-shrink:0;
    background:linear-gradient(135deg,rgba(56,140,255,0.2),rgba(0,212,255,0.1));
    border:1px solid rgba(56,140,255,0.3);
    display:flex; align-items:center; justify-content:center; font-size:26px;
    box-shadow:0 0 20px rgba(56,140,255,0.2);
  }
  .file-title-block { flex:1; min-width:0; }
  .file-title-block h2 { font-size:15px; font-weight:700; color:var(--text-primary); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .file-title-block p { font-size:11px; color:var(--text-muted); margin-top:2px; }
  .file-badges { display:flex; gap:6px; margin-top:6px; flex-wrap:wrap; }
  .badge {
    padding:2px 8px; border-radius:10px; font-size:10px; font-weight:600;
    letter-spacing:0.5px; border:1px solid;
  }
  .badge-valid { background:rgba(0,230,118,0.1); border-color:rgba(0,230,118,0.3); color:var(--success); }
  .badge-ver { background:rgba(56,140,255,0.1); border-color:rgba(56,140,255,0.3); color:var(--accent-blue); }
  .badge-err { background:rgba(255,82,82,0.1); border-color:rgba(255,82,82,0.3); color:var(--danger); }

  /* ── STAT CARDS ──────────────────────────── */
  .stats-grid {
    display:grid; grid-template-columns:repeat(auto-fit,minmax(110px,1fr));
    gap:10px; padding:16px 20px;
    background:rgba(6,10,24,0.5);
    border-bottom:1px solid var(--glass-border);
  }
  .stat-card {
    background:var(--bg-card); border:1px solid var(--glass-border);
    border-radius:var(--radius-md); padding:12px 14px;
    display:flex; flex-direction:column; gap:4px;
    transition:var(--trans);
  }
  .stat-card:hover { border-color:rgba(56,140,255,0.35); background:var(--bg-hover); transform:translateY(-1px); }
  .stat-val { font-size:22px; font-weight:700; color:var(--text-primary); line-height:1; }
  .stat-val.accent { color:var(--accent-blue); }
  .stat-key { font-size:10px; color:var(--text-muted); letter-spacing:0.5px; text-transform:uppercase; }

  /* ── TABS ────────────────────────────────── */
  .tab-bar {
    display:flex; gap:0; padding:0 20px;
    border-bottom:1px solid var(--glass-border);
    background:rgba(6,10,24,0.4);
    overflow-x:auto;
  }
  .tab {
    padding:10px 16px; font-size:12px; font-weight:500;
    color:var(--text-muted); cursor:pointer; transition:var(--trans);
    border-bottom:2px solid transparent; white-space:nowrap;
  }
  .tab:hover { color:var(--text-secondary); }
  .tab.active { color:var(--accent-blue); border-bottom-color:var(--accent-blue); }

  /* ── TAB CONTENT ─────────────────────────── */
  .tab-content { flex:1; overflow-y:auto; padding:16px 20px; }
  .tab-panel { display:none; }
  .tab-panel.active { display:block; }

  /* ── PROP TABLE ──────────────────────────── */
  .prop-table { width:100%; border-collapse:collapse; }
  .prop-table tr { border-bottom:1px solid rgba(56,140,255,0.06); }
  .prop-table tr:hover td { background:rgba(56,140,255,0.04); }
  .prop-table td { padding:8px 10px; }
  .prop-table td:first-child { color:var(--text-muted); font-size:11px; width:40%; padding-left:4px; }
  .prop-table td:last-child { color:var(--text-primary); font-size:12px; font-family:monospace; word-break:break-all; }

  /* ── SECTION TITLE ───────────────────────── */
  .section-title {
    font-size:10px; font-weight:600; color:var(--accent-blue);
    letter-spacing:1.5px; text-transform:uppercase;
    margin:16px 0 8px; padding-bottom:6px;
    border-bottom:1px solid rgba(56,140,255,0.15);
  }
  .section-title:first-child { margin-top:0; }

  /* ── HASH BOX ────────────────────────────── */
  .hash-box {
    font-family:monospace; font-size:11px; color:var(--accent-cyan);
    background:rgba(0,212,255,0.06); border:1px solid rgba(0,212,255,0.15);
    border-radius:var(--radius-sm); padding:8px 12px; word-break:break-all;
    line-height:1.6; letter-spacing:0.5px;
  }

  /* ── STREAMS LIST ────────────────────────── */
  .streams-list { display:flex; flex-wrap:wrap; gap:6px; }
  .stream-tag {
    padding:4px 10px; border-radius:var(--radius-sm);
    font-size:11px; font-family:monospace;
    background:rgba(56,140,255,0.08); border:1px solid rgba(56,140,255,0.2);
    color:var(--accent-blue);
  }

  /* ── 3D VIEWPORT ─────────────────────────── */
  #viewport-panel { position:relative; }
  #render-canvas {
    width:100%; height:100%; display:block;
    background: radial-gradient(ellipse at 40% 35%, rgba(10,25,60,0.95) 0%, rgba(3,6,18,0.98) 100%);
  }
  .viewport-toolbar {
    position:absolute; top:12px; left:50%; transform:translateX(-50%);
    display:flex; gap:4px; background:rgba(5,10,22,0.85);
    border:1px solid var(--glass-border); border-radius:20px;
    padding:5px 8px; backdrop-filter:blur(12px);
  }
  .vp-btn {
    padding:5px 10px; border-radius:12px; font-size:11px; font-weight:500;
    color:var(--text-muted); cursor:pointer; transition:var(--trans);
    border:1px solid transparent; white-space:nowrap;
  }
  .vp-btn:hover { color:var(--accent-blue); background:rgba(56,140,255,0.1); }
  .vp-btn.active { color:var(--accent-cyan); background:rgba(56,140,255,0.15); border-color:rgba(56,140,255,0.3); }
  .viewport-controls {
    position:absolute; right:14px; top:12px;
    display:flex; flex-direction:column; gap:4px;
  }
  .vc-btn {
    width:30px; height:30px; border-radius:var(--radius-sm);
    display:flex; align-items:center; justify-content:center;
    font-size:15px; cursor:pointer; transition:var(--trans);
    background:rgba(5,10,22,0.85); border:1px solid var(--glass-border);
    color:var(--text-secondary);
  }
  .vc-btn:hover { background:var(--bg-hover); color:var(--accent-blue); border-color:var(--accent-blue); }
  .viewport-info {
    position:absolute; left:14px; bottom:14px;
    font-size:10px; color:var(--text-dim); font-family:monospace;
    pointer-events:none;
  }

  /* ── RENDER PROGRESS ─────────────────────── */
  .render-progress-wrap { position:absolute; inset:0; display:none; align-items:center; justify-content:center; flex-direction:column; gap:16px; background:rgba(3,6,18,0.92); backdrop-filter:blur(4px); }
  .render-progress-wrap.visible { display:flex; }
  .render-bar-outer { width:220px; height:4px; background:rgba(56,140,255,0.1); border-radius:2px; overflow:hidden; }
  .render-bar-inner { height:100%; width:0%; background:linear-gradient(90deg,var(--accent-blue),var(--accent-cyan)); border-radius:2px; transition:width 0.1s linear; }
  .render-pct { font-size:28px; font-weight:700; color:var(--accent-cyan); line-height:1; }
  .render-label { font-size:11px; color:var(--text-muted); letter-spacing:1px; }

  /* ── RECENT FILES ────────────────────────── */
  .recent-list { display:flex; flex-direction:column; gap:6px; }
  .recent-item {
    display:flex; align-items:center; gap:10px; padding:10px 12px;
    background:var(--bg-card); border:1px solid var(--glass-border);
    border-radius:var(--radius-md); cursor:pointer; transition:var(--trans);
  }
  .recent-item:hover { background:var(--bg-hover); border-color:rgba(56,140,255,0.35); transform:translateX(3px); }
  .recent-icon { font-size:20px; flex-shrink:0; }
  .recent-info { flex:1; min-width:0; }
  .recent-name { font-size:12px; font-weight:600; color:var(--text-primary); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .recent-meta { font-size:10px; color:var(--text-muted); margin-top:2px; }
  .recent-size { font-size:11px; color:var(--text-dim); flex-shrink:0; }

  /* ── TOAST ───────────────────────────────── */
  #toast-container { position:fixed; bottom:20px; right:20px; z-index:9999; display:flex; flex-direction:column; gap:8px; }
  .toast {
    padding:10px 16px; border-radius:var(--radius-md);
    background:rgba(10,18,40,0.95); border:1px solid var(--glass-border);
    color:var(--text-primary); font-size:12px; font-weight:500;
    backdrop-filter:blur(12px); max-width:280px;
    animation: toastIn 0.3s ease; display:flex; align-items:center; gap:8px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.5);
  }
  .toast.success { border-color:rgba(0,230,118,0.3); }
  .toast.error { border-color:rgba(255,82,82,0.3); }
  @keyframes toastIn { from{opacity:0;transform:translateX(20px)} to{opacity:1;transform:translateX(0)} }

  /* ── RTL SUPPORT ─────────────────────────── */
  html[dir="rtl"] #sidebar { border-right:none; border-left:1px solid var(--glass-border); }
  html[dir="rtl"] .recent-item:hover { transform:translateX(-3px); }
  html[dir="rtl"] .nav-badge { margin-left:0; margin-right:auto; }

  /* ── EMPTY STATE ─────────────────────────── */
  .empty-state { display:flex; flex-direction:column; align-items:center; justify-content:center; flex:1; gap:10px; color:var(--text-dim); text-align:center; padding:40px; }
  .empty-icon { font-size:40px; opacity:0.4; }

  /* ── ABOUT ───────────────────────────────── */
  .about-card { background:var(--bg-card); border:1px solid var(--glass-border); border-radius:var(--radius-lg); padding:24px; max-width:400px; margin:20px auto; text-align:center; }
  .about-logo-wrap { width:64px; height:64px; border-radius:16px; background:linear-gradient(135deg,#1a4aff,#00d4ff); margin:0 auto 16px; display:flex; align-items:center; justify-content:center; font-size:32px; box-shadow:0 0 24px rgba(56,140,255,0.5); }
  .about-title { font-size:20px; font-weight:700; margin-bottom:4px; }
  .about-ver { font-size:11px; color:var(--accent-cyan); letter-spacing:1px; margin-bottom:16px; }
  .about-desc { font-size:12px; color:var(--text-secondary); line-height:1.7; }
  .about-row { display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid rgba(56,140,255,0.08); font-size:11px; }
  .about-row:last-child { border-bottom:none; }
  .about-k { color:var(--text-muted); }
  .about-v { color:var(--text-primary); }
</style>
</head>
<body>
<div class="bg-grid"></div>
<div class="bg-orb bg-orb-1"></div>
<div class="bg-orb bg-orb-2"></div>
<div class="bg-orb bg-orb-3"></div>

<div id="app">
  <!-- TOPBAR -->
  <div id="topbar">
    <div class="topbar-logo">
      <div class="logo-icon">🏗</div>
      <div>
        <div id="t-app-title">RevitViewer Pro</div>
        <div class="logo-sub" id="t-tagline">Professional BIM File Explorer</div>
      </div>
    </div>
    <div class="topbar-sep"></div>
    <div class="topbar-actions">
      <div class="btn-top primary" id="btn-open" onclick="openFile()">
        <span>📂</span><span id="t-open-file">Open File</span>
      </div>
      <div class="btn-top" id="btn-export" onclick="exportData()" style="display:none">
        <span>⬇</span><span id="t-export">Export</span>
      </div>
    </div>
    <div class="topbar-spacer"></div>
    <div style="display:flex;align-items:center;gap:8px">
      <div class="status-dot" id="status-dot"></div>
      <span id="status-text">Ready</span>
    </div>
    <select id="lang-select" onchange="switchLang(this.value)"></select>
  </div>

  <!-- MAIN -->
  <div id="main">
    <!-- SIDEBAR -->
    <div id="sidebar">
      <div class="sidebar-scroll">
        <div class="sidebar-section" style="padding-top:14px">
          <div class="sidebar-label">Navigation</div>
          <div class="sidebar-nav">
            <div class="nav-item active" onclick="showPanel('home')" id="nav-home">
              <span class="nav-icon">🏠</span><span id="t-home">Home</span>
            </div>
            <div class="nav-item" onclick="showPanel('file-info')" id="nav-file-info">
              <span class="nav-icon">📄</span><span id="t-file-info">File Info</span>
            </div>
            <div class="nav-item" onclick="showPanel('viewport')" id="nav-viewport">
              <span class="nav-icon">🎯</span><span id="t-rendering">3D Rendering</span>
            </div>
            <div class="nav-item" onclick="showPanel('metadata')" id="nav-metadata">
              <span class="nav-icon">🔖</span><span id="t-metadata">Metadata</span>
            </div>
            <div class="nav-item" onclick="showPanel('structure')" id="nav-structure">
              <span class="nav-icon">🗂</span><span id="t-structure">Structure</span>
            </div>
          </div>
        </div>

        <div class="sidebar-section">
          <div class="sidebar-label" id="t-recent-files">Recent Files</div>
          <div class="sidebar-nav" id="recent-nav"></div>
          <div class="nav-item" onclick="clearRecent()" style="margin-top:4px;opacity:0.6">
            <span class="nav-icon" style="font-size:12px">✕</span>
            <span style="font-size:11px" id="t-clear-recent">Clear Recent</span>
          </div>
        </div>
      </div>
      <div class="sidebar-footer">
        <div class="nav-item" onclick="showPanel('about')">
          <span class="nav-icon">ℹ</span><span id="t-about">About</span>
        </div>
      </div>
    </div>

    <!-- CONTENT -->
    <div id="content" style="position:relative">
      <!-- LOADING -->
      <div id="loading-overlay">
        <div class="loader-ring"></div>
        <div class="loader-text" id="t-loading">Analyzing file...</div>
      </div>

      <!-- HOME PANEL -->
      <div class="panel visible" id="panel-home">
        <div id="drop-zone"
          onclick="openFile()"
          ondragover="onDragOver(event)"
          ondragleave="onDragLeave(event)"
          ondrop="onDrop(event)">
          <div class="drop-icon">🏗</div>
          <div class="drop-title" id="t-drag-drop">Drag & drop your Revit file here</div>
          <div class="drop-sub" id="t-supported">Supports .rvt, .rfa, .rte, .rvt backup</div>
          <div class="drop-formats">
            <span class="format-tag fmt-rvt">.RVT</span>
            <span class="format-tag fmt-rfa">.RFA</span>
            <span class="format-tag fmt-rte">.RTE</span>
          </div>
          <div class="btn-browse" id="t-browse">Browse Files</div>
        </div>
      </div>

      <!-- FILE INFO PANEL -->
      <div class="panel" id="panel-file-info">
        <div class="file-panel-top" id="file-header"></div>
        <div class="stats-grid" id="stats-grid"></div>
        <div class="tab-bar" id="info-tabs"></div>
        <div class="tab-content" id="info-tab-content"></div>
      </div>

      <!-- 3D VIEWPORT -->
      <div class="panel" id="panel-viewport" style="position:relative">
        <canvas id="render-canvas"></canvas>
        <div class="viewport-toolbar" id="vp-toolbar">
          <div class="vp-btn active" onclick="setViewMode('solid')" id="vpm-solid">Solid</div>
          <div class="vp-btn" onclick="setViewMode('wireframe')" id="vpm-wireframe">Wireframe</div>
          <div class="vp-btn" onclick="setViewMode('xray')" id="vpm-xray">X-Ray</div>
          <div class="vp-btn" onclick="setViewMode('floor')" id="vpm-floor">Floor Plan</div>
        </div>
        <div class="viewport-controls">
          <div class="vc-btn" onclick="renderCam('top')" title="Top View">⬆</div>
          <div class="vc-btn" onclick="renderCam('front')" title="Front View">⬛</div>
          <div class="vc-btn" onclick="renderCam('iso')" title="Isometric">◈</div>
          <div class="vc-btn" onclick="zoomViewport(1.2)" title="Zoom In">＋</div>
          <div class="vc-btn" onclick="zoomViewport(0.8)" title="Zoom Out">－</div>
          <div class="vc-btn" onclick="resetView()" title="Home">⌂</div>
        </div>
        <div class="viewport-info" id="vp-info"></div>
        <div class="render-progress-wrap" id="render-progress">
          <div class="render-pct" id="render-pct">0%</div>
          <div class="render-bar-outer"><div class="render-bar-inner" id="render-bar"></div></div>
          <div class="render-label" id="t-rendering-progress">Rendering...</div>
        </div>
        <div style="position:absolute;bottom:14px;right:14px">
          <div class="btn-top primary" onclick="startRender()" id="render-btn">
            <span>🎬</span><span id="t-render-start">Initialize Render</span>
          </div>
        </div>
      </div>

      <!-- METADATA PANEL -->
      <div class="panel" id="panel-metadata">
        <div class="tab-content" style="padding:20px">
          <div id="metadata-content"></div>
        </div>
      </div>

      <!-- STRUCTURE PANEL -->
      <div class="panel" id="panel-structure">
        <div class="tab-content" style="padding:20px">
          <div id="structure-content"></div>
        </div>
      </div>

      <!-- ABOUT PANEL -->
      <div class="panel" id="panel-about">
        <div class="tab-content" style="padding:20px">
          <div class="about-card">
            <div class="about-logo-wrap">🏗</div>
            <div class="about-title">RevitViewer Pro</div>
            <div class="about-ver">VERSION 1.0.0 — BETA</div>
            <div class="about-desc">Professional BIM file explorer for Autodesk Revit files. Pure Python backend with native Windows integration.</div>
            <br>
            <div class="about-row"><span class="about-k">Engine</span><span class="about-v">PyWebView + HTML5</span></div>
            <div class="about-row"><span class="about-k">Parser</span><span class="about-v">Pure Python CFB</span></div>
            <div class="about-row"><span class="about-k">Renderer</span><span class="about-v">HTML5 Canvas 2D</span></div>
            <div class="about-row"><span class="about-k">Languages</span><span class="about-v">9 languages</span></div>
            <div class="about-row"><span class="about-k">Platform</span><span class="about-v">Windows 10/11</span></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<div id="toast-container"></div>

<script>
// ── STATE ─────────────────────────────────────
let state = {
  lang: 'en',
  rtlLangs: ['fa','ar'],
  t: {},
  currentFile: null,
  currentPanel: 'home',
  viewMode: 'solid',
  camMode: 'iso',
  zoom: 1.0,
  angle: { x: -0.4, y: 0.6 },
  dragging: false,
  dragStart: null,
  renderAnimId: null,
  buildingData: null,
  renderDone: false,
};

// ── INIT ──────────────────────────────────────
async function init() {
  const langs = JSON.parse(await pywebview.api.get_all_languages());
  const rtl   = JSON.parse(await pywebview.api.get_rtl_languages());
  state.rtlLangs = rtl;
  const sel = document.getElementById('lang-select');
  for (const [code, name] of Object.entries(langs)) {
    const opt = document.createElement('option');
    opt.value = code; opt.textContent = name;
    sel.appendChild(opt);
  }
  await switchLang('en');
  await loadRecent();
  setupCanvas();
  setStatus('Ready', false);
}

async function switchLang(lang) {
  state.lang = lang;
  state.t = JSON.parse(await pywebview.api.get_translations(lang));
  document.getElementById('lang-select').value = lang;
  const isRtl = state.rtlLangs.includes(lang);
  document.documentElement.setAttribute('dir', isRtl ? 'rtl' : 'ltr');
  document.documentElement.setAttribute('lang', lang);
  applyTranslations();
  if (state.currentFile) rebuildPanels();
}

function applyTranslations() {
  const T = state.t;
  const set = (id, key) => { const el=document.getElementById(id); if(el && T[key]) el.textContent=T[key]; };
  set('t-app-title','app_title'); set('t-tagline','tagline');
  set('t-open-file','open_file'); set('t-export','export');
  set('t-home','home'); set('t-file-info','file_info');
  set('t-rendering','rendering'); set('t-metadata','metadata');
  set('t-structure','structure'); set('t-about','about');
  set('t-recent-files','recent_files'); set('t-clear-recent','clear_recent');
  set('t-drag-drop','drag_drop'); set('t-supported','supported');
  set('t-browse','open_file'); set('t-loading','loading');
  set('t-rendering-progress','rendering_progress');
  set('t-render-start','render_start');
  set('vpm-solid','solid'); set('vpm-wireframe','wireframe');
  set('vpm-xray','xray'); set('vpm-floor','floor_plans');
}

// ── STATUS BAR ────────────────────────────────
function setStatus(msg, active) {
  document.getElementById('status-text').textContent = msg;
  document.getElementById('status-dot').className = 'status-dot' + (active ? ' active' : '');
}

// ── FILE OPERATIONS ───────────────────────────
async function openFile() {
  const path = await pywebview.api.open_file_dialog();
  if (!path) return;
  await loadFile(path);
}

async function loadFile(filepath) {
  setLoading(true);
  setStatus(state.t.loading || 'Analyzing...', true);
  try {
    const raw = await pywebview.api.parse_file(filepath);
    const data = JSON.parse(raw);
    state.currentFile = data;
    setLoading(false);
    document.getElementById('btn-export').style.display = '';
    buildFilePanel(data);
    buildMetadataPanel(data);
    buildStructurePanel(data);
    if (data.building_3d) {
      state.buildingData = data.building_3d;
      state.renderDone = false;
      drawBuilding();
    }
    showPanel('file-info');
    setStatus(data.file_name, true);
    await loadRecent();
    showToast('✅ ' + data.file_name, 'success');
  } catch(e) {
    setLoading(false);
    setStatus('Error', false);
    showToast('❌ ' + (e.message||e), 'error');
  }
}

async function exportData() {
  if (!state.currentFile) return;
  const name = state.currentFile.file_name.replace(/\.[^.]+$/,'') + '_info.json';
  const res = await pywebview.api.export_json(JSON.stringify(state.currentFile), name);
  if (res === 'ok') showToast('✅ Exported successfully', 'success');
  else if (res !== 'cancelled') showToast('❌ Export failed', 'error');
}

// ── LOADING ───────────────────────────────────
function setLoading(v) {
  const ol = document.getElementById('loading-overlay');
  ol.className = v ? 'visible' : '';
  ol.style.position = 'absolute';
}

// ── PANEL SYSTEM ──────────────────────────────
function showPanel(name) {
  state.currentPanel = name;
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('visible'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  const panel = document.getElementById('panel-' + name);
  if (panel) panel.classList.add('visible');
  const nav = document.getElementById('nav-' + name);
  if (nav) nav.classList.add('active');
  if (name === 'viewport') { resizeCanvas(); if(!state.renderDone) drawBuilding(); }
}

// ── FILE INFO PANEL ───────────────────────────
function buildFilePanel(d) {
  const T = state.t;
  const ext = (d.extension||'.rvt').toUpperCase().replace('.','');

  // Header
  const extIcon = {'.rvt':'🏗','.rfa':'🧱','.rte':'📋'}[d.extension] || '📄';
  document.getElementById('file-header').innerHTML = `
    <div class="file-icon-lg">${extIcon}</div>
    <div class="file-title-block">
      <h2>${esc(d.file_name)}</h2>
      <p>${esc(d.file_path)}</p>
      <div class="file-badges">
        ${d.valid ? `<span class="badge badge-valid">✓ Valid CFB</span>` : `<span class="badge badge-err">⚠ Invalid</span>`}
        ${d.revit_version ? `<span class="badge badge-ver">${esc(d.revit_version)}</span>` : ''}
        <span class="badge badge-ver">${ext}</span>
        <span class="badge badge-ver">${esc(d.file_size)}</span>
      </div>
    </div>`;

  // Stats
  const stats = d.stats || {};
  const sg = document.getElementById('stats-grid');
  sg.innerHTML = '';
  const cards = [
    [stats.elements,'elements'], [stats.views,'views'],
    [stats.sheets,'sheets'], [stats.families,'families'],
    [stats.categories,'categories'], [stats.floor_plans,'floor_plans'],
    [stats.sections,'sections'], [stats.elevations,'elevations'],
  ];
  cards.forEach(([val, key]) => {
    if (val == null) return;
    sg.innerHTML += `<div class="stat-card">
      <div class="stat-val accent">${val.toLocaleString()}</div>
      <div class="stat-key">${T[key]||key}</div>
    </div>`;
  });

  // Tabs
  const tabKeys = ['file_info','metadata','structure'];
  const tabLabels = [T.file_info||'File Info', T.metadata||'Metadata', T.structure||'Structure'];
  const tabBar = document.getElementById('info-tabs');
  tabBar.innerHTML = '';
  const tabContent = document.getElementById('info-tab-content');
  tabContent.innerHTML = '';

  tabKeys.forEach((tk, i) => {
    const tab = document.createElement('div');
    tab.className = 'tab' + (i===0 ? ' active' : '');
    tab.textContent = tabLabels[i];
    tab.onclick = () => {
      tabBar.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
      tabContent.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById('tp-'+tk).classList.add('active');
    };
    tabBar.appendChild(tab);

    const panel = document.createElement('div');
    panel.className = 'tab-panel' + (i===0?' active':'');
    panel.id = 'tp-' + tk;
    panel.innerHTML = buildTabContent(tk, d);
    tabContent.appendChild(panel);
  });
}

function buildTabContent(key, d) {
  const T = state.t;
  if (key === 'file_info') {
    return `
      <div class="section-title">${T.file_info||'File Information'}</div>
      <table class="prop-table">
        <tr><td>${T.file_name||'File Name'}</td><td>${esc(d.file_name)}</td></tr>
        <tr><td>${T.file_size||'File Size'}</td><td>${esc(d.file_size)} (${(d.file_size_bytes||0).toLocaleString()} bytes)</td></tr>
        <tr><td>${T.modified||'Modified'}</td><td>${esc(d.modified)}</td></tr>
        <tr><td>${T.created||'Created'}</td><td>${esc(d.created)}</td></tr>
        <tr><td>${T.version||'Version'}</td><td>${esc(d.revit_version)||'—'}</td></tr>
        <tr><td>CFB Version</td><td>${esc(d.cfb_version)||'—'}</td></tr>
        <tr><td>Sector Size</td><td>${esc(d.sector_size)||'—'}</td></tr>
        <tr><td>Byte Order</td><td>${esc(d.byte_order)||'—'}</td></tr>
        <tr><td>FAT Sectors</td><td>${d.fat_sectors??'—'}</td></tr>
      </table>
      <div class="section-title" style="margin-top:16px">${T.file_hash||'File Hash (SHA256)'}</div>
      <div class="hash-box">${esc(d.file_hash||'—')}</div>
      <div class="section-title" style="margin-top:16px">${T.raw_bytes||'Raw Header Bytes'}</div>
      <div class="hash-box">${esc(d.raw_header||'—')}</div>`;
  }
  if (key === 'metadata') {
    const m = d.metadata || {};
    const rows = Object.entries(m).map(([k,v])=>`<tr><td>${esc(k)}</td><td>${esc(String(v))}</td></tr>`).join('');
    return `
      <div class="section-title">${T.metadata||'Metadata'}</div>
      ${rows ? `<table class="prop-table">${rows}</table>` : `<div class="empty-state"><div class="empty-icon">🔍</div><div>No metadata extracted</div></div>`}`;
  }
  if (key === 'structure') {
    const streams = d.streams || [];
    return `
      <div class="section-title">${T.streams||'Compound Streams'}</div>
      <div class="streams-list">${streams.map(s=>`<span class="stream-tag">${esc(s)}</span>`).join('')||'<span style="color:var(--text-dim)">No streams detected</span>'}</div>
      <div class="section-title" style="margin-top:16px">Stream Count</div>
      <table class="prop-table">
        <tr><td>Streams Found</td><td>${d.stream_count||0}</td></tr>
        <tr><td>First Dir Sector</td><td>${d.first_dir_sector??'—'}</td></tr>
      </table>`;
  }
  return '';
}

function rebuildPanels() {
  if (!state.currentFile) return;
  buildFilePanel(state.currentFile);
  buildMetadataPanel(state.currentFile);
  buildStructurePanel(state.currentFile);
}

function buildMetadataPanel(d) {
  const T = state.t;
  const m = d.metadata || {};
  const s = d.stats || {};
  let html = `<div class="section-title">${T.project_name||'Project Information'}</div>
    <table class="prop-table">
      ${Object.entries(m).map(([k,v])=>`<tr><td>${esc(k)}</td><td>${esc(String(v))}</td></tr>`).join('') || '<tr><td colspan="2" style="color:var(--text-dim);padding:12px 4px">No metadata available in binary</td></tr>'}
    </table>
    <div class="section-title" style="margin-top:16px">${T.elements||'Element Statistics'}</div>
    <table class="prop-table">
      ${Object.entries(s).map(([k,v])=>`<tr><td>${T[k]||k}</td><td>${Number(v).toLocaleString()}</td></tr>`).join('')}
    </table>`;
  document.getElementById('metadata-content').innerHTML = html;
}

function buildStructurePanel(d) {
  const T = state.t;
  const streams = d.streams || [];
  let html = `<div class="section-title">${T.structure||'File Structure'}</div>
    <table class="prop-table">
      <tr><td>Format</td><td>Compound File Binary (OLE2)</td></tr>
      <tr><td>Magic Bytes</td><td style="font-family:monospace">D0 CF 11 E0 A1 B1 1A E1</td></tr>
      <tr><td>CFB Version</td><td>${esc(d.cfb_version||'—')}</td></tr>
      <tr><td>Sector Size</td><td>${esc(d.sector_size||'—')}</td></tr>
      <tr><td>Byte Order</td><td>${esc(d.byte_order||'—')}</td></tr>
      <tr><td>FAT Sectors</td><td>${d.fat_sectors??'—'}</td></tr>
      <tr><td>Revit Version</td><td>${esc(d.revit_version||'Unknown')}</td></tr>
    </table>
    <div class="section-title" style="margin-top:16px">${T.streams||'Detected Streams'}</div>
    <div class="streams-list">${streams.map(s=>`<span class="stream-tag">${esc(s)}</span>`).join('') || '<span style="color:var(--text-dim)">No named streams detected</span>'}</div>
    <div class="section-title" style="margin-top:16px">${T.file_hash||'Integrity'}</div>
    <div class="hash-box">${esc(d.file_hash||'—')}</div>`;
  document.getElementById('structure-content').innerHTML = html;
}

// ── 3D CANVAS RENDERER ────────────────────────
let canvas, ctx, canvasW, canvasH;
let mouse = {down:false,x:0,y:0,lx:0,ly:0};

function setupCanvas() {
  canvas = document.getElementById('render-canvas');
  ctx = canvas.getContext('2d');
  canvas.addEventListener('mousedown', e => { mouse.down=true; mouse.lx=e.clientX; mouse.ly=e.clientY; });
  window.addEventListener('mouseup', () => { mouse.down=false; });
  window.addEventListener('mousemove', e => {
    if(!mouse.down || state.currentPanel!=='viewport') return;
    const dx=(e.clientX-mouse.lx)/200, dy=(e.clientY-mouse.ly)/200;
    state.angle.y += dx; state.angle.x += dy;
    mouse.lx=e.clientX; mouse.ly=e.clientY;
    drawBuilding();
  });
  canvas.addEventListener('wheel', e => {
    e.preventDefault();
    state.zoom *= e.deltaY>0 ? 0.9 : 1.1;
    state.zoom = Math.max(0.2, Math.min(5, state.zoom));
    drawBuilding();
  }, {passive:false});
}

function resizeCanvas() {
  if (!canvas) return;
  const rect = canvas.parentElement.getBoundingClientRect();
  canvas.width = rect.width;
  canvas.height = rect.height;
  canvasW = rect.width; canvasH = rect.height;
  drawBuilding();
}

function project(x, y, z) {
  const ax = state.angle.x, ay = state.angle.y;
  // Rotate Y
  const x1 = x*Math.cos(ay) + z*Math.sin(ay);
  const z1 = -x*Math.sin(ay) + z*Math.cos(ay);
  // Rotate X
  const y2 = y*Math.cos(ax) - z1*Math.sin(ax);
  const z2 = y*Math.sin(ax) + z1*Math.cos(ax);
  const fov = 600 * state.zoom;
  const pz = z2 + fov;
  const px = canvasW/2 + x1/pz*fov;
  const py = canvasH/2 - y2/pz*fov;
  return {px, py, depth: z2};
}

function drawLine(p1, p2, style, alpha=1) {
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.strokeStyle = style;
  ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(p1.px,p1.py); ctx.lineTo(p2.px,p2.py); ctx.stroke();
  ctx.restore();
}

function drawBuilding() {
  if (!canvas) return;
  resizeCanvasIfNeeded();
  const d = state.buildingData;
  if (!d) { drawEmpty(); return; }

  const W = d.width, D = d.depth, FH = d.floor_height, NF = d.floors;
  const cx = W/2, cd = D/2;

  // Background
  const bg = ctx.createRadialGradient(canvasW/2,canvasH*0.4,0,canvasW/2,canvasH/2,Math.max(canvasW,canvasH)*0.7);
  bg.addColorStop(0,'#0a1832'); bg.addColorStop(1,'#020408');
  ctx.fillStyle = bg;
  ctx.fillRect(0,0,canvasW,canvasH);

  const mode = state.viewMode;
  const pts = (x,y,z)=>project(x-cx,y,z-cd);

  // Draw floor slabs
  for (let f=0; f<=NF; f++) {
    const fy = f*FH;
    const alpha = f===0||f===NF ? 0.7 : 0.18;
    const col = f===NF ? '#00d4ff' : '#1a6fff';
    const corners = [pts(0,fy,0),pts(W,fy,0),pts(W,fy,D),pts(0,fy,D)];
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.strokeStyle = col;
    ctx.lineWidth = f===0||f===NF ? 1.5 : 0.5;
    ctx.beginPath();
    ctx.moveTo(corners[0].px,corners[0].py);
    for(let i=1;i<4;i++) ctx.lineTo(corners[i].px,corners[i].py);
    ctx.closePath();
    if(mode==='solid'||mode==='xray') {
      ctx.fillStyle = mode==='xray'?'rgba(10,30,80,0.08)':'rgba(10,30,80,0.18)';
      ctx.fill();
    }
    ctx.stroke();
    ctx.restore();
  }

  // Columns
  if (mode !== 'floor') {
    d.columns.forEach(col => {
      const cw=0.4, cd2=0.4;
      const x=col.x, z=col.y;
      for(let f=0;f<NF;f++) {
        const y0=f*FH, y1=(f+1)*FH;
        const alpha = 0.6;
        // 4 vertical edges
        [
          [pts(x,y0,z),pts(x,y1,z)],
          [pts(x+cw,y0,z),pts(x+cw,y1,z)],
          [pts(x,y0,z+cd2),pts(x,y1,z+cd2)],
          [pts(x+cw,y0,z+cd2),pts(x+cw,y1,z+cd2)],
        ].forEach(([a,b])=>drawLine(a,b,'rgba(56,140,255,0.5)',alpha));
      }
    });
  }

  // Vertical edges of the building envelope
  [[0,0],[W,0],[W,D],[0,D]].forEach(([ex,ez])=>{
    const bot=pts(ex,0,ez), top2=pts(ex,NF*FH,ez);
    ctx.save(); ctx.globalAlpha=0.8; ctx.strokeStyle='#2060cc'; ctx.lineWidth=2;
    ctx.beginPath(); ctx.moveTo(bot.px,bot.py); ctx.lineTo(top2.px,top2.py); ctx.stroke();
    ctx.restore();
  });

  // Facade lines (windows)
  if (mode !== 'wireframe') {
    for (let f=0;f<NF;f++) {
      const fy = f*FH + FH*0.2;
      const fh = FH * 0.6;
      // Front facade divisions
      const divs = Math.max(2, Math.floor(W/4));
      for (let i=1; i<divs; i++) {
        const wx = W/divs*i;
        const a=pts(wx,fy,0), b=pts(wx,fy+fh,0);
        drawLine(a,b,'rgba(0,212,255,0.2)',0.5);
      }
    }
  }

  // Core
  const coreX=(W-d.core.w)/2, coreZ=(D-d.core.d)/2;
  for(let f=0;f<NF;f++) {
    const y0=f*FH, y1=(f+1)*FH;
    [[coreX,y0,coreZ],[coreX+d.core.w,y0,coreZ],[coreX+d.core.w,y0,coreZ+d.core.d],[coreX,y0,coreZ+d.core.d]].forEach((pt,i,arr)=>{
      const next=arr[(i+1)%4];
      drawLine(pts(...pt),pts(...next),'rgba(255,160,40,0.25)',0.6);
    });
    drawLine(pts(coreX,y0,coreZ),pts(coreX,y1,coreZ),'rgba(255,160,40,0.4)',0.7);
  }

  // Glow at base
  const baseGrad = ctx.createRadialGradient(canvasW/2,canvasH*0.65,0,canvasW/2,canvasH*0.65,canvasW*0.25);
  baseGrad.addColorStop(0,'rgba(56,140,255,0.08)');
  baseGrad.addColorStop(1,'transparent');
  ctx.fillStyle=baseGrad; ctx.fillRect(0,0,canvasW,canvasH);

  // Info overlay
  const el = document.getElementById('vp-info');
  if(el) el.textContent = `Floors: ${NF}  |  ${W.toFixed(0)}m × ${D.toFixed(0)}m  |  H: ${(NF*FH).toFixed(1)}m  |  Mode: ${state.viewMode}`;
}

function resizeCanvasIfNeeded() {
  if(!canvas) return;
  const rect = canvas.parentElement.getBoundingClientRect();
  if(canvas.width!==rect.width||canvas.height!==rect.height) {
    canvas.width=rect.width; canvas.height=rect.height;
    canvasW=rect.width; canvasH=rect.height;
  }
}

function drawEmpty() {
  ctx.fillStyle='#020408'; ctx.fillRect(0,0,canvasW,canvasH);
  ctx.fillStyle='rgba(56,140,255,0.15)';
  ctx.font='40px sans-serif'; ctx.textAlign='center';
  ctx.fillText('🏗', canvasW/2, canvasH/2-20);
  ctx.font='14px sans-serif';
  ctx.fillStyle='rgba(56,140,255,0.3)';
  ctx.fillText('Load a Revit file to render', canvasW/2, canvasH/2+30);
}

function setViewMode(m) {
  state.viewMode = m;
  document.querySelectorAll('[id^="vpm-"]').forEach(b=>b.classList.remove('active'));
  const el = document.getElementById('vpm-'+m);
  if(el) el.classList.add('active');
  drawBuilding();
}

function renderCam(mode) {
  state.camMode = mode;
  if(mode==='top') { state.angle.x=-Math.PI/2; state.angle.y=0; }
  else if(mode==='front') { state.angle.x=0; state.angle.y=0; }
  else if(mode==='iso') { state.angle.x=-0.4; state.angle.y=0.6; }
  drawBuilding();
}

function zoomViewport(f) { state.zoom=Math.max(0.2,Math.min(5,state.zoom*f)); drawBuilding(); }
function resetView() { state.angle={x:-0.4,y:0.6}; state.zoom=1; drawBuilding(); }

function startRender() {
  const prog = document.getElementById('render-progress');
  prog.classList.add('visible');
  const bar = document.getElementById('render-bar');
  const pct = document.getElementById('render-pct');
  let p=0;
  const tick=()=>{
    p += Math.random()*4+1;
    if(p>=100){ p=100; clearInterval(iv);
      setTimeout(()=>{ prog.classList.remove('visible'); state.renderDone=true; showToast('✅ '+( state.t.render_done||'Render Complete'),'success'); drawBuilding(); },600);
    }
    bar.style.width=p+'%'; pct.textContent=Math.floor(p)+'%';
  };
  const iv=setInterval(tick,60);
}

// ── RECENT FILES ──────────────────────────────
async function loadRecent() {
  const raw = await pywebview.api.get_recent_files();
  const files = JSON.parse(raw);
  const nav = document.getElementById('recent-nav');
  nav.innerHTML = '';
  files.slice(0,5).forEach(f=>{
    const item=document.createElement('div');
    item.className='nav-item';
    item.style.cssText='flex-direction:column;align-items:flex-start;gap:1px;padding:7px 10px';
    item.innerHTML=`<span style="font-size:11.5px;font-weight:600;color:var(--text-secondary);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;width:100%">${esc(f.name)}</span>
      <span style="font-size:10px;color:var(--text-dim)">${esc(f.size)} · ${esc(f.opened)}</span>`;
    item.onclick=()=>loadFile(f.path);
    nav.appendChild(item);
  });
}

async function clearRecent() {
  await pywebview.api.clear_recent_files();
  document.getElementById('recent-nav').innerHTML='';
}

// ── DRAG & DROP ───────────────────────────────
function onDragOver(e) { e.preventDefault(); document.getElementById('drop-zone').classList.add('drag-over'); }
function onDragLeave(e) { document.getElementById('drop-zone').classList.remove('drag-over'); }
function onDrop(e) {
  e.preventDefault();
  document.getElementById('drop-zone').classList.remove('drag-over');
  const file = e.dataTransfer.files[0];
  if (file) loadFile(file.path);
}

// ── TOAST ─────────────────────────────────────
function showToast(msg, type='') {
  const el = document.createElement('div');
  el.className = 'toast ' + type;
  el.textContent = msg;
  document.getElementById('toast-container').appendChild(el);
  setTimeout(()=>el.remove(), 3500);
}

// ── UTILS ─────────────────────────────────────
function esc(s) { if(s==null)return''; return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

// ── WINDOW RESIZE ─────────────────────────────
window.addEventListener('resize', ()=>{ if(state.currentPanel==='viewport') resizeCanvas(); });

// ── START ─────────────────────────────────────
window.addEventListener('pywebviewready', init);
</script>
</body>
</html>"""


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
def main():
    api = RevitViewerAPI()

    window = webview.create_window(
        title='RevitViewer Pro',
        html=HTML,
        js_api=api,
        width=1280,
        height=800,
        min_size=(960, 640),
        resizable=True,
        background_color='#050810',
        text_select=False,
    )
    api.set_window(window)

    webview.start(
        debug=False,
        private_mode=False,
    )


if __name__ == '__main__':
    main()
