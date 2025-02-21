import torch
import torch.nn as nn
def attack(model, image, eps = 8/255, itr = 10):
    image.requires_grad = True
    criterion = nn.CrossEntropyLoss()
    _, original_label = model(image).data.max(1)
    curr_image = torch.clamp((image + (torch.rand_like(image) - 0.5) * 4 * eps), -1, 1).data
    if itr == 1:
        stepsize = 2 * eps
    else:
        stepsize = 2 * eps * 5 / itr
    for _ in range(itr):
        curr_image.requires_grad = True
        curr_logits = model(curr_image)
        loss = criterion(curr_logits, original_label)
        model.zero_grad()
        loss.backward()
        grad_sign = curr_image.grad.data.sign()
        curr_image = torch.clamp(
            torch.clamp(
                curr_image + grad_sign * stepsize - image,
                 -eps * 2, eps * 2) + image,
             -1,1
        ).data
    return curr_image

def attack_feature(model, image, eps = 8/255, itr = 10, loss_type = 'l1'):
    image.requires_grad = True
    original_feature = model.feature(image).data
    curr_image = torch.clamp((image + (torch.rand_like(image) - 0.5) * 4 * eps), -1, 1).data
    if itr == 1:
        stepsize = 2 * eps
    else:
        setpsize = 2 * eps * 5 / itr
    if loss_type == 'l1':
        criterion = nn.L1Loss()
    elif loss_type == 'l2':
        criterion = nn.MSELoss() 
    for _ in range(itr):
        curr_image.requires_grad = True
        curr_feature = model.feature(curr_image)
        loss = criterion(curr_feature, original_feature)
        model.zero_grad()
        loss.backward()
        grad_sign = curr_image.grad.data.sign()
        curr_image = torch.clamp(
            torch.clamp(
                curr_image + grad_sign * stepsize  - image,
                 -eps * 2, eps * 2) + image,
             -1,1
        ).data
    return curr_image
