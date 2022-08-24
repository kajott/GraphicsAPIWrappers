def wrappers(m):
    m.title = "Graphics API Wrapper Matrix"
    m.coltitle = "Source API"
    m.rowtitle = "Target API"

    d3d7  = m.add_category("Direct3D 7/8")
    d3d9  = m.add_category("Direct3D 9")
    d3d11 = m.add_category("Direct3D 11")
    d3d12 = m.add_category("Direct3D 12")
    gl    = m.add_category("Desktop OpenGL")
    gles1 = m.add_category("OpenGL ES 1.x")
    gles2 = m.add_category("OpenGL ES 2.x/3.x")
    vk    = m.add_category("Vulkan")
    mtl   = m.add_category("Metal")

    in_mesa = m.add_footnote('implemented as part of the <a href="https://www.mesa3d.org" target="_blank">Mesa</a> project')

    # specific wrappers
    m.add_item((d3d9, d3d11),       vk,             "DXVK",         "https://github.com/doitsujin/dxvk")
    m.add_item( d3d12,              vk,             "VKD3D",        "https://wiki.winehq.org/Vkd3d")
    m.add_item( d3d12,              vk,             "VKD3D-Proton", "https://github.com/HansKristian-Work/vkd3d-proton")
    m.add_item( d3d9,               d3d11,          "DXUP",         "https://github.com/Joshua-Ashton/dxup")
    m.add_item( d3d9,               d3d12,          "D3D9On12",     "https://github.com/microsoft/D3D9On12")
    m.add_item( d3d11,              d3d12,          "D3D11On12",    "https://github.com/microsoft/D3D11On12")
    m.add_item( vk,                 mtl,            "MoltenVK",     "https://github.com/KhronosGroup/MoltenVK")
    m.add_item( gl,                 vk,             "Zink",         "https://docs.mesa3d.org/drivers/zink.html")
    m.add_item( gl,                 gles2,          "GL4ES",        "http://ptitseb.github.io/gl4es/")
    m.add_item( gl,                 d3d12,          "OpenGLOn12",   "https://docs.mesa3d.org/drivers/d3d12.html", in_mesa)
    m.add_item( vk,                 d3d12,          "Dozen",        "https://gitlab.freedesktop.org/mesa/mesa/-/tree/main/src/microsoft/vulkan", in_mesa)

    # universal wrappers
    m.add_item( gles2, (gl, d3d9, d3d11, gles2, vk, mtl),  "ANGLE", "https://chromium.googlesource.com/angle/angle/+/main/README.md")
    m.add_item((d3d7, d3d9, d3d11), (gl, vk),       "WineD3D",      "https://www.winehq.org")
    m.add_item((d3d7, d3d9),        (d3d11, d3d12), "dgVoodoo 2",   "http://dege.freeweb.hu/dgVoodoo2/")
