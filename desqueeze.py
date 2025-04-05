import os
import cv2


squeezed_folder = '2025_04_04_alum_2'
squeeze_factor = 1.33
downsample = False

def main():
    save_path = os.path.join(squeezed_folder, 'desqueeze')
    print(os.getcwd())
    if not os.path.isdir(save_path):
        print(f'{save_path} not found, creating {save_path}')
        os.mkdir(save_path)
    for image_path in os.listdir(squeezed_folder):
        print(image_path)
        # only read images, handle videos later
        if '.png' in image_path.lower() or '.jpg' in image_path.lower():
            read_image_path = os.path.join(squeezed_folder, image_path)
            print(f'read: {read_image_path}')
            image = cv2.imread(read_image_path)

            r,c = image.shape[:2]

            # assume anamorphic lens is on horizontally, so the longer of the two dimensions is the one that needs to be desqueezed

            # these are the dimensions if we upsample, this will cause interpolation but will preserve all of the original data

            if r > c:
                target_r = squeeze_factor * r
                target_c = c
            else:
                target_r = r
                target_c = squeeze_factor * c

            if downsample:
                # downsample will throw away some data, but won't introduce new pixels
                # technically interpolation will happen here too
                # why is this better than cropping? data is thrown out uniformly across the vertical band instead of just at the edges, IMO primarily makes a difference when shooting

                # to downsample, we want the original number of rows to be the same 
                if r > c:
                    target_r = r / squeeze_factor
                    target_c = c
                else:
                    target_r = r
                    target_c = c / squeeze_factor
            target_r = int(target_r)
            target_c = int(target_c)
            # do resample
            # try different resampling techniques here, but @cchen TODO implement from scratch
            desqueeze_image = cv2.resize(image, (target_c, target_r), interpolation=cv2.INTER_CUBIC)

            write_path = os.path.join(save_path, image_path)

            print(f'write desqueeze to : {write_path}')
            cv2.imwrite(write_path, desqueeze_image)

            



if __name__=='__main__':
    main()