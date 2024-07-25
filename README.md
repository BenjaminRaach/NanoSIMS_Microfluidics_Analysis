ToDo-List:
- Look how the updated rotate_image file influences the overall code
- Update all the Code with use of ChatGTP




Why is this code needed?
- NanoSIMS images have the problem that they are deformed and in multiple smaller images.
- Segmentaion of cells does not work for NanoSIMS, because the borders are unclear, often cells look merged
- Deformations are large
- To combine the single-cell growth data from the microfluidics experiments with the isotopic data from NanoSIMS, we need to overlay the segmentation mask, which are generated from the microfluidics data with the NanoSIMS data.
- The approach we chose uses cross-correlation to refine the overlap step-by-step
- Therefore, the approximate position (x,y position; angle; and rescale) NanoSIMS image is determined
- Than the image is split into N smaller images (Each image should have a size of 5x5 cell lengths)
- The more precise position (x,y position; angle; and rescale) is again determined by cross-correlation within a predefined range of its previously determined position (x,y position; angle; and rescale)


General assumptions:
- This appraoch assumes that on a small scale deformations are neglitable
