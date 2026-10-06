#!/usr/bin/env python3
"""
Arina Luxury Brand - 4K Commercial Video Suite Generator
Renders cinematic brand films and social reels with authentic Arina typography,
Luxor Gold graphics, and high-fidelity ambient stereo audio.
"""

import os
import shutil
import subprocess

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, 'output', 'videos')
IMAGERY_DIR = os.path.join(WORKSPACE_DIR, 'output', 'imagery')
SCRATCH_DIR = os.path.join(WORKSPACE_DIR, 'scratch', 'video_build')

FONT_ARABIC_BOLD = '/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf'
FONT_ARABIC_REG = '/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf'
FONT_LATIN_BOLD = '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'
FONT_LATIN_ITALIC = '/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf'
FONT_SANS_BOLD = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SCRATCH_DIR, exist_ok=True)


def generate_ambient_audio(duration, out_path):
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', f'sine=frequency=110:d={duration}',
        '-f', 'lavfi', '-i', f'sine=frequency=165:d={duration}',
        '-f', 'lavfi', '-i', f'sine=frequency=220:d={duration}',
        '-f', 'lavfi', '-i', f'sine=frequency=330:d={duration}',
        '-filter_complex',
        f'[0:a]volume=0.25[a0];[1:a]volume=0.18[a1];[2:a]volume=0.14[a2];[3:a]volume=0.10[a3];'
        f'[a0][a1][a2][a3]amix=inputs=4,lowpass=f=350,afade=t=in:ss=0:d=1.5,afade=t=out:st={duration-1.5}:d=1.5[out]',
        '-map', '[out]',
        '-c:a', 'aac', '-b:a', '192k',
        out_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def save_dual_video(src_path, canonical_name):
    dst_canonical = os.path.join(OUTPUT_DIR, canonical_name)
    dst_legacy = os.path.join(OUTPUT_DIR, canonical_name.replace('arina_', 'mariam_'))
    shutil.copy2(src_path, dst_canonical)
    shutil.copy2(src_path, dst_legacy)
    print(f'[SAVED VIDEO DUAL] {dst_canonical} & {dst_legacy}')


def render_brand_film_4k():
    print('Rendering Video 1: Arina Master Brand Film 4K...')
    audio_path = os.path.join(SCRATCH_DIR, 'brand_film_audio.aac')
    generate_ambient_audio(24, audio_path)

    scenes = [
        ('arina_commercial_ad_grand_mediterranean_connoisseur_board_4k.jpg',
         'ARINA — MADE WITH LOVE', 'مجموعة أرينا المتوسطية الحرفية الكبرى'),
        ('arina_commercial_ad_the_acoustic_snap_cucumbers_4k.jpg',
         'CRISP BABY CUCUMBERS & DILL', 'الخيار الصغير المقرمش بماء الينابيع والخل الطبيعي'),
        ('arina_commercial_ad_the_ruby_terroir_turnips_4k.jpg',
         'WILD TURNIP & NATURAL BEETROOT', 'اللفت البلدي المعتّق بخلاصة الشمندر الطبيعي الياقوتي'),
        ('arina_commercial_ad_pure_unroasted_garlic_farm_fresh_4k.jpg',
         'PURE CRUSHED GARLIC — UNROASTED', 'ثوم مهروس طازج نقي 100% بدون شوي وبدون إضافات'),
        ('arina_commercial_ad_hand_stuffed_almond_olives_4k.jpg',
         'HAND-STUFFED ARTISANAL OLIVES', 'زيتون أخضر ملكي محشي يدوياً بحبة لوز مقرمشة كاملة'),
        ('arina_grand_regal_15_jar_three_tier_pyramid_exhibition_4k.jpg',
         'ARINA — THE ART OF MEDITERRANEAN TASTE', 'أرينا: صُنع بحب لنخبة الذواقة')
    ]

    subclips = []
    for idx, (img_fn, title_en, title_ar) in enumerate(scenes):
        clip_p = os.path.join(SCRATCH_DIR, f'bf_sub_{idx}.mp4')
        img_p = os.path.join(IMAGERY_DIR, img_fn)
        if not os.path.exists(img_p):
            img_p = os.path.join(IMAGERY_DIR, img_fn.replace('arina_', 'mariam_'))

        vf = (
            f"scale=3840:2160,zoompan=z='min(zoom+0.0006,1.08)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=3840x2160:fps=30,"
            f"drawtext=fontfile={FONT_LATIN_BOLD}:text='{title_en}':fontcolor=0xDAAC36:fontsize=56:x=(w-text_w)/2:y=180,"
            f"drawtext=fontfile={FONT_ARABIC_BOLD}:text='{title_ar}':fontcolor=0x1E3326:fontsize=52:x=(w-text_w)/2:y=260,"
            f"fade=t=in:st=0:d=0.5,fade=t=out:st=3.5:d=0.5"
        )
        cmd = [
            'ffmpeg', '-y', '-loop', '1', '-i', img_p,
            '-vf', vf, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-t', '4',
            clip_p
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subclips.append(clip_p)

    list_p = os.path.join(SCRATCH_DIR, 'bf_list.txt')
    with open(list_p, 'w') as f:
        for c in subclips:
            f.write(f"file '{c}'\n")

    tmp_out = os.path.join(SCRATCH_DIR, 'arina_master_brand_film_4k_tmp.mp4')
    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', list_p,
        '-i', audio_path,
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest',
        tmp_out
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    save_dual_video(tmp_out, 'arina_master_brand_film_4k.mp4')


def render_royal_crunch_reel():
    print('Rendering Video 2: Arina Social Reel - The Royal Crunch 9:16...')
    audio_path = os.path.join(SCRATCH_DIR, 'reel1_audio.aac')
    generate_ambient_audio(15, audio_path)

    scenes = [
        ('arina_commercial_ad_the_acoustic_snap_cucumbers_4k.jpg',
         'اسمع صوت القرمشة الحقيقية!', 'THE ROYAL ACOUSTIC SNAP', 'خيار صغير مقرمش بماء الينابيع والخل الطبيعي'),
        ('arina_ruby_and_emerald_duo_spectacle_4k.jpg',
         '100% لون طبيعي بدون أي صبغات!', 'RUBY & EMERALD TERROIR', 'ياقوت الشمندر المركز مع قرمشة اللفت البلدي'),
        ('arina_commercial_ad_pure_unroasted_garlic_farm_fresh_4k.jpg',
         'ثوم طازج نقي وكأنه قُطف وهُرس الآن!', 'FARM-FRESH UNROASTED PURITY', 'وداعاً للتقشير والرائحة العالقة... جودة الشيف الفاخرة'),
        ('arina_commercial_ad_hand_stuffed_almond_olives_4k.jpg',
         'حبة زيتون محشوة بحبة لوز كاملة!', 'HAND-STUFFED ARTISANAL OLIVES', 'حرفية يدوية فاخرة تعتز بها موائد الذواقة'),
        ('arina_complete_gastronomy_trinity_hero_4k.jpg',
         'أرينا: صُنع بحب لنخبة الموائد', 'ORDER YOUR LUXURY JAR TODAY', 'متوفر الآن في أفخر نقاط البيع والمتجر الإلكتروني')
    ]

    subclips = []
    for idx, (img_fn, hook_ar, tag_en, sub_ar) in enumerate(scenes):
        clip_p = os.path.join(SCRATCH_DIR, f'rc_sub_{idx}.mp4')
        img_p = os.path.join(IMAGERY_DIR, img_fn)
        if not os.path.exists(img_p):
            img_p = os.path.join(IMAGERY_DIR, img_fn.replace('arina_', 'mariam_'))

        vf = (
            f"scale=1080:-1,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=white,"
            f"zoompan=z='min(zoom+0.0015,1.15)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,"
            f"drawtext=fontfile={FONT_ARABIC_BOLD}:text='{hook_ar}':fontcolor=0x1E3326:fontsize=52:x=(w-text_w)/2:y=240,"
            f"drawtext=fontfile={FONT_LATIN_BOLD}:text='{tag_en}':fontcolor=0xDAAC36:fontsize=36:x=(w-text_w)/2:y=315,"
            f"drawtext=fontfile={FONT_ARABIC_REG}:text='{sub_ar}':fontcolor=0x555555:fontsize=32:x=(w-text_w)/2:y=1660,"
            f"fade=t=in:st=0:d=0.3,fade=t=out:st=2.7:d=0.3"
        )
        cmd = [
            'ffmpeg', '-y', '-loop', '1', '-i', img_p,
            '-vf', vf, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-t', '3',
            clip_p
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subclips.append(clip_p)

    list_p = os.path.join(SCRATCH_DIR, 'rc_list.txt')
    with open(list_p, 'w') as f:
        for c in subclips:
            f.write(f"file '{c}'\n")

    tmp_out = os.path.join(SCRATCH_DIR, 'arina_royal_crunch_tmp.mp4')
    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', list_p,
        '-i', audio_path,
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest',
        tmp_out
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    save_dual_video(tmp_out, 'arina_social_reel_the_royal_crunch_9x16.mp4')


def render_garlic_spotlight_reel():
    print('Rendering Video 3: Arina Garlic Revolution Spotlight 9:16...')
    audio_path = os.path.join(SCRATCH_DIR, 'reel2_audio.aac')
    generate_ambient_audio(12, audio_path)

    scenes = [
        ('arina_commercial_ad_pure_unroasted_garlic_farm_fresh_4k.jpg',
         'ثوم مهروس طازج غير مشوي (210g & 100g)', 'PURE UNROASTED CRUSHED GARLIC', 'سحر النكهة الطازجة الفورية لأطباقك اليومية'),
        ('arina_commercial_ad_cloud_whipped_toum_4k.jpg',
         'معجون التوم المخفوق كالسحاب (210g & 100g)', 'THE CLOUD-WHIPPED TOUM', 'قوام مخملي ناصع البياض بنكهة متوسطية أصيلة'),
        ('arina_garlic_connoisseur_tasting_trinity_hero_4k.jpg',
         'ثالوث الثوم الملكي من أرينا', 'THE COMPLETE GARLIC TRINITY', 'توم مخفوق • ثوم مهروس طازج • ثوم مشوي ببطء')
    ]

    subclips = []
    for idx, (img_fn, hook_ar, tag_en, sub_ar) in enumerate(scenes):
        clip_p = os.path.join(SCRATCH_DIR, f'gr_sub_{idx}.mp4')
        img_p = os.path.join(IMAGERY_DIR, img_fn)
        if not os.path.exists(img_p):
            img_p = os.path.join(IMAGERY_DIR, img_fn.replace('arina_', 'mariam_'))

        vf = (
            f"scale=1080:-1,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=white,"
            f"zoompan=z='min(zoom+0.0012,1.12)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,"
            f"drawtext=fontfile={FONT_ARABIC_BOLD}:text='{hook_ar}':fontcolor=0x1E3326:fontsize=48:x=(w-text_w)/2:y=240,"
            f"drawtext=fontfile={FONT_LATIN_BOLD}:text='{tag_en}':fontcolor=0xDAAC36:fontsize=36:x=(w-text_w)/2:y=310,"
            f"drawtext=fontfile={FONT_ARABIC_REG}:text='{sub_ar}':fontcolor=0x555555:fontsize=32:x=(w-text_w)/2:y=1660,"
            f"fade=t=in:st=0:d=0.4,fade=t=out:st=3.6:d=0.4"
        )
        cmd = [
            'ffmpeg', '-y', '-loop', '1', '-i', img_p,
            '-vf', vf, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-t', '4',
            clip_p
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subclips.append(clip_p)

    list_p = os.path.join(SCRATCH_DIR, 'gr_list.txt')
    with open(list_p, 'w') as f:
        for c in subclips:
            f.write(f"file '{c}'\n")

    tmp_out = os.path.join(SCRATCH_DIR, 'arina_garlic_tmp.mp4')
    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', list_p,
        '-i', audio_path,
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest',
        tmp_out
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    save_dual_video(tmp_out, 'arina_garlic_revolution_spotlight_9x16.mp4')


def render_pyramid_flythrough_4k():
    print('Rendering Video 4: Arina 15-Jar Pyramid 3D Sweep 4K...')
    audio_path = os.path.join(SCRATCH_DIR, 'pyramid_audio.aac')
    generate_ambient_audio(10, audio_path)

    img_p = os.path.join(IMAGERY_DIR, 'arina_grand_regal_15_jar_three_tier_pyramid_exhibition_4k.jpg')
    if not os.path.exists(img_p):
        img_p = os.path.join(IMAGERY_DIR, 'mariam_grand_regal_15_jar_three_tier_pyramid_exhibition_4k.jpg')

    vf = (
        f"scale=3840:2160,zoompan=z='1.12-0.0008*on':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=3840x2160:fps=30,"
        f"drawtext=fontfile={FONT_LATIN_BOLD}:text='ARINA — THE 15-JAR GRAND REGAL EXHIBITION':fontcolor=0xDAAC36:fontsize=64:x=(w-text_w)/2:y=180,"
        f"drawtext=fontfile={FONT_ARABIC_BOLD}:text='الهرم الإمبراطوري الأكبر: 15 خط إنتاج فاخر من أرينا في برطمانات زجاجية':fontcolor=0x1E3326:fontsize=52:x=(w-text_w)/2:y=270,"
        f"fade=t=in:st=0:d=1.0,fade=t=out:st=8.8:d=1.2"
    )
    tmp_out = os.path.join(SCRATCH_DIR, 'arina_pyramid_tmp.mp4')
    cmd = [
        'ffmpeg', '-y', '-loop', '1', '-i', img_p,
        '-i', audio_path,
        '-vf', vf, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-t', '10',
        '-c:a', 'aac', '-b:a', '192k', '-shortest',
        tmp_out
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    save_dual_video(tmp_out, 'arina_pyramid_exhibition_3d_flythrough_4k.mp4')


def main():
    print("=" * 70)
    print("RENDERING ALL 4 ARINA COMMERCIAL VIDEOS (CINEMA 4K & SOCIAL REELS)")
    print("=" * 70)
    render_brand_film_4k()
    render_royal_crunch_reel()
    render_garlic_spotlight_reel()
    render_pyramid_flythrough_4k()
    print("=" * 70)
    print("ALL 4 ARINA COMMERCIAL VIDEOS RENDERED AND DEPLOYED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == '__main__':
    main()
