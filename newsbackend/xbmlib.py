#!/usr/bin/python
# -*- coding: utf-8 -*-
''' prepares images feed for eink devies '''

import cairocffi as cairo
import sys
import cairocffi
import cffi


ffi = cffi.FFI()
ffi.include(cairocffi.ffi)
ffi.cdef('''
    /* GLib */
    typedef void* gpointer;
    void g_object_unref (gpointer object);

    /* Pango and PangoCairo */
    typedef ... PangoLayout;
    typedef enum {
        PANGO_ALIGN_LEFT,
        PANGO_ALIGN_CENTER,
        PANGO_ALIGN_RIGHT
    } PangoAlignment;
    int pango_units_from_double (double d);
    PangoLayout * pango_cairo_create_layout (cairo_t *cr);
    void pango_cairo_show_layout (cairo_t *cr, PangoLayout *layout);
    void pango_layout_set_width (PangoLayout *layout, int width);
    void pango_layout_set_alignment (
        PangoLayout *layout, PangoAlignment alignment);
    void pango_layout_set_markup (
        PangoLayout *layout, const char *text, int length);
''')
gobject = ffi.dlopen('gobject-2.0')
pango = ffi.dlopen('pango-1.0')
pangocairo = ffi.dlopen('pangocairo-1.0')

gobject_ref = lambda pointer: ffi.gc(pointer, gobject.g_object_unref)
units_from_double = pango.pango_units_from_double


surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 320, 120)
context = cairo.Context(surf)

#draw a background rectangle:
context.rectangle(0,0,320,120)
context.set_source_rgb(1, 1, 1)
context.fill()

#get font families:

font_map = pangocairo.cairo_font_map_get_default()
families = font_map.list_families()

# to see family names:
print [f.get_name() for f in   font_map.list_families()]

#context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

# Positions drawing origin so that the text desired top-let corner is at 0,0
context.translate(50,25)

pangocairo_context = pangocairo.CairoContext(context)
pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

layout = pangocairo_context.create_layout()
fontname = sys.argv[1] if len(sys.argv) >= 2 else "Sans"
font = pango.FontDescription(fontname + " 25")
layout.set_font_description(font)

layout.set_text(u"Travis L.")
context.set_source_rgb(0, 0, 0)
pangocairo_context.update_layout(layout)
pangocairo_context.show_layout(layout)

with open("cairo_text.png", "wb") as image_file:
    surf.write_to_png(image_file)