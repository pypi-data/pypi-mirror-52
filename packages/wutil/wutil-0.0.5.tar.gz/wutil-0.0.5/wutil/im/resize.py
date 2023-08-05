import cv2


def resize_preserve_aspect(im, max_side_size, interpolation=cv2.INTER_CUBIC):
    """ Resize image to fixed max side size.

    Returns
    -------
    res_im : numpy array
        resized image
    h_scale : float
        vertical scale used for resize
    w_scale : float
        horizontal scale used for resize

    """
    h, w = im.shape[:2]
    if h > w:
        h_scale = h / max_side_size
        w_scale = h_scale
    else:
        w_scale = w / max_side_size
        h_scale = w_scale

    target_size = round(w / w_scale), round(h / h_scale)
    res_im = cv2.resize(im, target_size, interpolation=interpolation)
    return res_im, h_scale, w_scale

