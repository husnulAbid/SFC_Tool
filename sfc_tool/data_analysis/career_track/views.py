from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Django (must be before pyplot import)
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import os
from datetime import datetime
from PIL import Image
import requests
from io import BytesIO



class CareerTrackView(APIView):
    def get(self, request):
        logo_path = "data_analysis/career_track/temp_logo"
        output_path = "data_analysis/career_track/temp_logo/output"
        datetime_now = datetime.now()
        datetime_value = datetime_now.strftime('%Y%m%d%H%M%S')
        datetime_value_display = datetime_now.strftime('%Y-%m-%d %H:%M:%S')

        timeline = CareerTimeline(background_color='white', want_institution_name=False)

        timeline.add_entry("2015-2016", "BD", "Bachelor's Student", "United International University", f"{logo_path}/uiu.png", y_base=0.5, position='top', logo_size=0.8)
        timeline.add_entry("2017", "DE", "Exchange Student", "Universität Bremen", f"{logo_path}/uni_bremen.png", y_base=0.5, position='bottom', logo_size=1.0)
        timeline.add_entry("2018-2019", "BD", "Teaching Assistant", "United International University", f"{logo_path}/uiu.png", y_base=0.5, position='top', logo_size=0.8)
        timeline.add_entry("2020-2022", "BD", "Software Engineer", "Niftycoders", f"{logo_path}/niftycoders.png", y_base=0.5, position='bottom', logo_size=1.0)
        timeline.add_entry("2022", "FI", "Research Assistant", "Åbo Akademi University", f"{logo_path}/aau.png", y_base=0.5, position='top', logo_size=1.2)
        timeline.add_entry("2023", "SE", "Scrum Master", "Mälardalen University", f"{logo_path}/mdu.png", y_base=0.5, position='bottom', logo_size=1.0)
        timeline.add_entry("2023", "SE", "ML Engineer", "RISE", f"{logo_path}/rise.png", y_base=0.5, position='top', logo_size=0.7)
        timeline.add_entry("2024", "FI", "Data Scientist", "Creanord", f"{logo_path}/creanord.png", y_base=0.5, position='bottom', logo_size=1.0)
        timeline.add_entry("2025 - Pres", "FI", "Software Engineer", "Innopipe AI", f"{logo_path}/innopipe.png", y_base=0.5, position='top', logo_size=1.2)

        timeline.render_career_track(f"{output_path}/career_timeline_{datetime_value}.png")

        return Response({"message": f"It's done at {datetime_value_display}!"}, status=status.HTTP_200_OK) 



def get_flag_image(country_code):
    url = f"https://flagcdn.com/w80/{country_code.lower()}.png"
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


class CareerTimeline:
    def __init__(self, figsize=(18, 6), background_color='white', want_institution_name=True):
        self.data = []
        self.figsize = figsize
        self.background_color = background_color
        self.want_institution_name = want_institution_name


    def add_entry(self, year_range, country, role, organization, logo_path=None, y_base=0.5, position='top', logo_size=1.0):
        self.data.append({
            "year_range": year_range,
            "country": country,
            "role": role,
            "organization": organization,
            "logo_path": logo_path,
            "y_base": y_base,
            "position": position,
            "logo_size": logo_size
        })


    def draw_arrow(self, ax, x, box_width, bar_height):
        arrow_shape = [
            (x - box_width / 2, -bar_height),
            (x + box_width / 2 - 0.2, -bar_height),
            (x + box_width / 2, 0),
            (x + box_width / 2 - 0.2, bar_height),
            (x - box_width / 2, bar_height),
            (x - box_width / 2 + 0.2, 0)
        ]
        arrow = patches.Polygon(arrow_shape, closed=True, color="#1f4e79")
        ax.add_patch(arrow)


    def add_year_text(self, ax, x, year_range):
        ax.text(x, 0, year_range, ha='center', va='center', fontsize=13, color='white')


    def draw_vertical_line(self, ax, x, bar_height, y_base, direction):
        gap = 0.05
        ax.plot([x, x], [bar_height * direction + gap * direction, y_base * direction], linestyle="--", lw=2, color="#1c48d1")


    def add_text_labels(self, ax, x, item, direction, y_base):
        if self.want_institution_name:
            # With institution names - normal spacing
            role_y = y_base * direction + 0.3 * direction
            org_y = y_base * direction + 0.15 * direction
            ax.text(x, role_y, item['role'], ha='center', fontsize=12, weight='bold')
            ax.text(x, org_y, item['organization'], ha='center', fontsize=12)
        else:
            # Without institution names - closer spacing
            role_y = y_base * direction + 0.15 * direction
            ax.text(x, role_y, item['role'], ha='center', fontsize=12)


    def draw_flag(self, ax, x, country_code, direction):
        country_y = -0.20 * direction
        
        try:
            flag_img = get_flag_image(country_code)
            img_ratio = flag_img.height / flag_img.width
            flag_size = 0.30

            # Draw black rectangle border
            ax.add_patch(patches.Rectangle(
                (x - flag_size, country_y - flag_size * (img_ratio * 0.4)),
                flag_size * 2,  # Width
                flag_size * (img_ratio * 0.8),  # Height
                linewidth=1,
                edgecolor='black',
                facecolor='none'
            ))

            ax.imshow(flag_img, extent=[
                x - flag_size,
                x + flag_size,
                country_y - flag_size * (img_ratio * 0.4),
                country_y + flag_size * (img_ratio * 0.4)
            ], aspect='auto')
        except Exception as e:
            print(f"Flag error for {country_code}: {e}")


    def get_logo_extent_strict(self, x, y, img, logo_size=1.0):
        img_h, img_w = img.shape[:2]
        aspect = img_w / img_h

        buckets = [0.5, 0.8, 1.0, 1.5, 2.0]
        snapped = min(buckets, key=lambda r: abs(r - aspect))

        if snapped == 0.5:
            width, height = 0.50, 0.50
        elif snapped == 0.8:
            width, height = 0.80, 0.45
        elif snapped == 1.0:
            width, height = 1.00, 0.40
        elif snapped == 1.5:
            width, height = 1.50, 0.30
        elif snapped == 2.0:
            width, height = 2.00, 0.20
        else:
            width, height = 1.00, 0.40

        width *= logo_size
        height *= logo_size

        return [x - width / 2, x + width / 2, y - height / 2, y + height / 2]
        

    def draw_logo(self, ax, x, logo_path, y_base, direction, logo_size=1.0):
        if logo_path and os.path.exists(logo_path):
            try:
                img = mpimg.imread(logo_path)
                
                # Adjust logo position based on whether institution names are shown
                if self.want_institution_name:
                    # With institution names - normal spacing
                    logo_offset = 0.65 if direction == 1 else 0.50
                else:
                    # Without institution names - closer spacing
                    logo_offset = 0.45 if direction == 1 else 0.35
                
                logo_y = y_base * direction + logo_offset * direction

                extent = self.get_logo_extent_strict(x, logo_y, img, logo_size)
                ax.imshow(img, extent=extent, aspect='auto')
            except Exception as e:
                print(f"Error loading logo: {e}")


    def finalize_plot(self, ax, output_path):
        ax.set_xlim(-1, len(self.data) * 2.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_axis_off()
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300)
        else:
            plt.show()


    def render_career_track(self, output_path=None):
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Set background color
        fig.patch.set_facecolor(self.background_color)
        ax.set_facecolor(self.background_color)

        for idx, item in enumerate(self.data):
            x = idx * 1.9  
            box_width = 2.0
            bar_height = 0.09 
            y_base = item.get("y_base", 0.5)
            pos = item.get("position", 'top')
            direction = 1 if pos == 'top' else -1

            self.draw_arrow(ax, x, box_width, bar_height)
            self.add_year_text(ax, x, item['year_range'])
            self.draw_vertical_line(ax, x, bar_height, y_base, direction)
            self.add_text_labels(ax, x, item, direction, y_base)
            self.draw_flag(ax, x, item['country'], direction)
            self.draw_logo(ax, x, item['logo_path'], y_base, direction, item.get('logo_size', 1.0))

        self.finalize_plot(ax, output_path)