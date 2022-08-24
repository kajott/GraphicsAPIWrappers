def wrappers(m):
    m.title = "Graphics API Wrapper Matrix"

    d3d7  = m.add_category("Direct3D 7/8")
    d3d9  = m.add_category("Direct3D 9")
    d3d11 = m.add_category("Direct3D 11")
    d3d12 = m.add_category("Direct3D 12")
    gl    = m.add_category("Desktop OpenGL")
    gles1 = m.add_category("OpenGL ES 1.x")
    gles2 = m.add_category("OpenGL ES 2.x/3.x")
    vk    = m.add_category("Vulkan")
    mtl   = m.add_category("Metal")

    m.add_item((d3d9, d3d11), vk,    "DXVK",     "https://github.com/doitsujin/dxvk")
    m.add_item( d3d9,         d3d11, "DXUP",     "https://github.com/Joshua-Ashton/dxup")
    m.add_item( d3d9,         d3d12, "D3D9on12", "https://github.com/microsoft/D3D9On12")
