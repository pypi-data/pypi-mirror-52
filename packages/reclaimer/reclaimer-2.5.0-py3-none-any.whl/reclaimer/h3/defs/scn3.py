############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: DarkShallFall
# 	Widgets, Bitmaps, Animations, Y and X offsets, layers, blending, and model.
# revision: 3		author: -DeToX-
# 	X and Y Scale
# revision: 4		author: Lord Zedd
# 	Fixed up, added flags and types
# revision: 5		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


scn3_data_source = Struct("data_source", 
    h3_dependency("data_source"),
    ENDIAN=">", SIZE=16
    )


scn3_group_widget_list_widget_list_widget_item = Struct("list_widget_item", 
    Bool32("flags", *unknown_flags_32),
    h3_string_id("name"),
    SInt16("unknown", VISIBLE=False),
    SInt16("layer"),
    SInt16("widescreen_y_offset"),
    SInt16("widescreen_x_offset"),
    SInt16("widescreen_y_unknown"),
    SInt16("widescreen_x_unknown"),
    SInt16("standard_y_offset"),
    SInt16("standard_x_offset"),
    SInt16("standard_y_unknown"),
    SInt16("standard_x_unknown"),
    h3_dependency("animation"),
    h3_string_id("target"),
    ENDIAN=">", SIZE=48
    )


scn3_group_widget_list_widget = Struct("list_widget", 
    h3_dependency("ancestor"),
    Bool32("flags", 
        ("horizontal", 1 << 4),
        "loops",
        ),
    h3_string_id("name"),
    SInt16("unknown", VISIBLE=False),
    SInt16("layer"),
    SInt16("widescreen_y_offset"),
    SInt16("widescreen_x_offset"),
    SInt16("widescreen_y_unknown"),
    SInt16("widescreen_x_unknown"),
    SInt16("standard_y_offset"),
    SInt16("standard_x_offset"),
    SInt16("standard_y_unknown"),
    SInt16("standard_x_unknown"),
    h3_dependency("animation"),
    h3_string_id("data_source_name"),
    h3_dependency("skin"),
    SInt32("row_count"),
    h3_reflexive("list_widget_items", scn3_group_widget_list_widget_list_widget_item),
    h3_dependency("up_arrow_bitmap"),
    h3_dependency("down_arrow_bitmap"),
    ENDIAN=">", SIZE=128
    )


scn3_group_widget_text_widget = Struct("text_widget", 
    h3_dependency("ancestor"),
    Bool32("flags", 
        ("left_alignment", 1 << 3),
        "right_alignment",
        ("all_caps", 1 << 6),
        ("wrap_at_bounds", 1 << 13),
        ),
    h3_string_id("name"),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("layer"),
    SInt16("widescreen_y_bounds_min"),
    SInt16("widescreen_x_bounds_min"),
    SInt16("widescreen_y_bounds_max"),
    SInt16("widescreen_x_bounds_max"),
    SInt16("standard_y_bounds_min"),
    SInt16("standard_x_bounds_min"),
    SInt16("standard_y_bounds_max"),
    SInt16("standard_x_bounds_max"),
    h3_dependency("animation"),
    h3_string_id("data_source_name"),
    h3_string_id("text_string"),
    h3_string_id("text_color"),
    SInt16("text_font"),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=76
    )


scn3_group_widget_bitmap_widget = Struct("bitmap_widget", 
    h3_dependency("ancestor"),
    Bool32("flags", 
        ("scale_to_bounds", 1 << 3),
        "replace_with_blur",
        ("replace_with_white", 1 << 10),
        "replace_with_black",
        ),
    h3_string_id("name"),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("layer"),
    SInt16("widescreen_y_bounds_min"),
    SInt16("widescreen_x_bounds_min"),
    SInt16("widescreen_y_bounds_max"),
    SInt16("widescreen_x_bounds_max"),
    SInt16("standard_y_bounds_min"),
    SInt16("standard_x_bounds_min"),
    SInt16("standard_y_bounds_max"),
    SInt16("standard_x_bounds_max"),
    h3_dependency("animation"),
    h3_dependency("bitmap"),
    h3_dependency("unknown_1"),
    SEnum16("blend_method", *bmp3_blend_method),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("sprite_index"),
    SInt16("unknown_3", VISIBLE=False),
    h3_string_id("data_source_name"),
    h3_string_id("sprite_data_source_name"),
    ENDIAN=">", SIZE=108
    )


scn3_group_widget_model_widget_camera_refinement_zoom_data_1 = Struct("zoom_data_1", 
    h3_rawdata_ref("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


scn3_group_widget_model_widget_camera_refinement_zoom_data_2 = Struct("zoom_data_2", 
    h3_rawdata_ref("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


scn3_group_widget_model_widget_camera_refinement = Struct("camera_refinement", 
    h3_string_id("biped", VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=8, VISIBLE=False),
    h3_reflexive("zoom_data_1", scn3_group_widget_model_widget_camera_refinement_zoom_data_1),
    h3_reflexive("zoom_data_2", scn3_group_widget_model_widget_camera_refinement_zoom_data_2),
    VISIBLE=False,
    ENDIAN=">", SIZE=60
    )


scn3_group_widget_model_widget = Struct("model_widget", 
    h3_dependency("ancestor"),
    Bool32("flags", *unknown_flags_32),
    h3_string_id("name"),
    SInt16("unknown", VISIBLE=False),
    SInt16("layer"),
    SInt16("widescreen_y_bounds_min"),
    SInt16("widescreen_x_bounds_min"),
    SInt16("widescreen_y_bounds_max"),
    SInt16("widescreen_x_bounds_max"),
    SInt16("standard_y_bounds_min"),
    SInt16("standard_x_bounds_min"),
    SInt16("standard_y_bounds_max"),
    SInt16("standard_x_bounds_max"),
    h3_dependency("animation"),
    h3_reflexive("camera_refinement", scn3_group_widget_model_widget_camera_refinement),
    ENDIAN=">", SIZE=72
    )


scn3_group_widget = Struct("group_widget", 
    h3_dependency("ancestor"),
    Bool32("flags", 
        ("initially_hidden", 1 << 3),
        ),
    h3_string_id("name"),
    SInt16("unknown", VISIBLE=False),
    SInt16("layer"),
    SInt16("widescreen_y_offset"),
    SInt16("widescreen_x_offset"),
    SInt16("widescreen_y_unknown"),
    SInt16("widescreen_x_unknown"),
    SInt16("standard_y_offset"),
    SInt16("standard_x_offset"),
    SInt16("standard_y_unknown"),
    SInt16("standard_x_unknown"),
    h3_dependency("animation"),
    h3_reflexive("list_widgets", scn3_group_widget_list_widget),
    h3_reflexive("text_widgets", scn3_group_widget_text_widget),
    h3_reflexive("bitmap_widgets", scn3_group_widget_bitmap_widget),
    h3_reflexive("model_widgets", scn3_group_widget_model_widget),
    ENDIAN=">", SIZE=108
    )


scn3_button_key_legend = Struct("button_key_legend", 
    h3_dependency("legend"),
    ENDIAN=">", SIZE=16
    )


scn3_body = Struct("tagdata", 
    Bool32("flags", *unknown_flags_32),
    h3_string_id("name"),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("layer"),
    SInt16("widescreen_y_bounds_min"),
    SInt16("widescreen_x_bounds_min"),
    SInt16("widescreen_y_bounds_max"),
    SInt16("widescreen_x_bounds_max"),
    SInt16("standard_y_bounds_min"),
    SInt16("standard_x_bounds_min"),
    SInt16("standard_y_bounds_max"),
    SInt16("standard_x_bounds_max"),
    h3_dependency("animation"),
    h3_dependency("strings"),
    h3_dependency("ancestor"),
    h3_string_id("default_key_legend_string"),
    h3_reflexive("data_sources", scn3_data_source),
    h3_reflexive("group_widgets", scn3_group_widget),
    h3_reflexive("button_key_legends", scn3_button_key_legend),
    h3_dependency("ui_sounds"),
    ascii_str32("script_title"),
    SInt16("script_index"),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=168
    )


def get():
    return scn3_def

scn3_def = TagDef("scn3",
    h3_blam_header('scn3'),
    scn3_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["scn3"], endian=">", tag_cls=H3Tag
    )