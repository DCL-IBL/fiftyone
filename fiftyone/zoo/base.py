"""
FiftyOne Zoo Datasets provided natively by the library.

| Copyright 2017-2020, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import logging
import os
import shutil

import eta.core.utils as etau
import eta.core.web as etaw

import fiftyone.types as fot
import fiftyone.utils.bdd as foub
import fiftyone.utils.coco as fouc

# import fiftyone.utils.cityscapes as foucs
import fiftyone.utils.data as foud
import fiftyone.utils.hmdb51 as fouh
import fiftyone.utils.lfw as foul
import fiftyone.utils.ucf101 as fouu
import fiftyone.zoo as foz


logger = logging.getLogger(__name__)


class FiftyOneDataset(foz.ZooDataset):
    """Base class for zoo datasets that are provided natively by FiftyOne."""

    pass


class QuickstartDataset(FiftyOneDataset):
    """A small dataset with ground truth bounding boxes and predictions.

    The dataset consists of 200 images from the validation split of COCO-2017,
    with model predictions generated by an out-of-the-box Faster R-CNN model
    from ``torchvision.models``.

    Dataset size:
        23.4MB
    """

    _GDRIVE_ID = "1UWTlFmdq8H-wdJHxVsAKpXBilY1CWwm_"
    _DIR_IN_ZIP = "quickstart"

    @property
    def name(self):
        return "quickstart"

    @property
    def supported_splits(self):
        return None

    def _download_and_prepare(self, dataset_dir, scratch_dir, _):
        # Download dataset
        tmp_zip_path = os.path.join(scratch_dir, "dataset.zip")
        etaw.download_google_drive_file(self._GDRIVE_ID, path=tmp_zip_path)

        # Extract zip
        logger.info("Extracting dataset")
        etau.extract_zip(tmp_zip_path, delete_zip=True)
        _move_dir(os.path.join(scratch_dir, self._DIR_IN_ZIP), dataset_dir)

        # Get metadata
        logger.info("Parsing dataset metadata")
        dataset_type = fot.FiftyOneDataset()
        importer = foud.FiftyOneDatasetImporter
        classes = importer.get_classes(dataset_dir)
        num_samples = importer.get_num_samples(dataset_dir)
        logger.info("Found %d samples", num_samples)

        return dataset_type, num_samples, classes


class VideoQuickstartDataset(FiftyOneDataset):
    """A small video dataset with dense annotations.

    The dataset consists of 10 video segments with dense object detections
    generated by human annotators.

    Dataset size:
        35.2MB
    """

    _GDRIVE_ID = "1O-WMjtiBBMXGEHnnus6y2nSlJu8pY5vo"
    _DIR_IN_ZIP = "quickstart-video"

    @property
    def name(self):
        return "quickstart-video"

    @property
    def supported_splits(self):
        return None

    def _download_and_prepare(self, dataset_dir, scratch_dir, _):
        # Download dataset
        tmp_zip_path = os.path.join(scratch_dir, "dataset.zip")
        etaw.download_google_drive_file(self._GDRIVE_ID, path=tmp_zip_path)

        # Extract zip
        logger.info("Extracting dataset")
        etau.extract_zip(tmp_zip_path, delete_zip=True)
        _move_dir(os.path.join(scratch_dir, self._DIR_IN_ZIP), dataset_dir)

        # Get metadata
        logger.info("Parsing dataset metadata")
        dataset_type = fot.FiftyOneVideoLabelsDataset()
        num_samples = foud.FiftyOneVideoLabelsDatasetImporter.get_num_samples(
            dataset_dir
        )
        logger.info("Found %d samples", num_samples)

        return dataset_type, num_samples, None


class COCO2014Dataset(FiftyOneDataset):
    """COCO is a large-scale object detection, segmentation, and captioning
    dataset.

    This version contains images, bounding boxes, segmentations, and labels for
    the 2014 version of the dataset.

    Notes:
        - COCO defines 91 classes but the data only uses 80 classes
        - some images from the train and validation sets don't have annotations
        - the test set does not have annotations
        - COCO 2014 and 2017 uses the same images, but different train/val/test
            splits

    Dataset size:
        37.57 GiB

    Source:
        http://cocodataset.org/#home
    """

    @property
    def name(self):
        return "coco-2014-segmentation"

    @property
    def supported_splits(self):
        return ("test", "train", "validation")

    def _download_and_prepare(self, dataset_dir, scratch_dir, split):
        # Download dataset
        images_dir, anno_path = fouc.download_coco_dataset_split(
            scratch_dir, split, year="2014", cleanup=True
        )

        # Build dataset
        logger.info("Organizing dataset")
        data_dir = os.path.join(dataset_dir, "data")
        labels_path = os.path.join(dataset_dir, "labels.json")
        etau.move_dir(images_dir, data_dir)
        etau.move_file(anno_path, labels_path)

        logger.info("Parsing dataset metadata")
        dataset_type = fot.COCODetectionDataset()
        _, classes, _, images, _ = fouc.load_coco_detection_annotations(
            labels_path
        )
        num_samples = len(images)
        logger.info("Found %d samples", num_samples)

        return dataset_type, num_samples, classes


class COCO2017Dataset(FiftyOneDataset):
    """COCO is a large-scale object detection, segmentation, and captioning
    dataset.

    This version contains images, bounding boxes, segmentations, and labels for
    the 2017 version of the dataset.

    Notes:
        - COCO defines 91 classes but the data only uses 80 classes
        - some images from the train and validation sets don't have annotations
        - the test set does not have annotations
        - COCO 2014 and 2017 uses the same images, but different train/val/test
            splits

    Dataset size:
        25.20 GiB

    Source:
        http://cocodataset.org/#home
    """

    @property
    def name(self):
        return "coco-2017-segmentation"

    @property
    def supported_splits(self):
        return ("test", "train", "validation")

    def _download_and_prepare(self, dataset_dir, scratch_dir, split):
        # Download dataset
        images_dir, anno_path = fouc.download_coco_dataset_split(
            scratch_dir, split, year="2017", cleanup=True
        )

        # Build dataset
        logger.info("Organizing dataset")
        data_dir = os.path.join(dataset_dir, "data")
        labels_path = os.path.join(dataset_dir, "labels.json")
        etau.move_dir(images_dir, data_dir)
        etau.move_file(anno_path, labels_path)

        logger.info("Parsing dataset metadata")
        dataset_type = fot.COCODetectionDataset()
        _, classes, _, images, _ = fouc.load_coco_detection_annotations(
            labels_path
        )
        num_samples = len(images)
        logger.info("Found %d samples", num_samples)

        return dataset_type, num_samples, classes


class LabeledFacesInTheWildDataset(FiftyOneDataset):
    """Labeled Faces in the Wild is a public benchmark for face verification,
    also known as pair matching.

    The dataset contains 13,233 images of 5,749 people's faces collected from
    the web. Each face has been labeled with the name of the person pictured.
    1,680 of the people pictured have two or more distinct photos in the data
    set. The only constraint on these faces is that they were detected by the
    Viola-Jones face detector.

    Dataset size:
        173 MB

    Source:
        http://vis-www.cs.umass.edu/lfw
    """

    @property
    def name(self):
        return "lfw"

    @property
    def supported_splits(self):
        return ("test", "train")

    def _download_and_prepare(self, dataset_dir, scratch_dir, split):
        #
        # LFW is distributed as a single download that contains all splits,
        # so we remove the split from `dataset_dir` and download the whole
        # dataset (only if necessary)
        #
        dataset_dir = os.path.dirname(dataset_dir)  # remove split dir
        split_dir = os.path.join(dataset_dir, split)
        if not os.path.exists(split_dir):
            foul.download_lfw_dataset(
                dataset_dir, scratch_dir=scratch_dir, cleanup=False
            )

        # Get metadata
        logger.info("Parsing dataset metadata")
        dataset_type = fot.ImageClassificationDirectoryTree()
        importer = foud.ImageClassificationDirectoryTreeImporter
        classes = sorted(
            importer.get_classes(os.path.join(dataset_dir, "train"))
            + importer.get_classes(os.path.join(dataset_dir, "test"))
        )
        num_samples = importer.get_num_samples(split_dir)
        logger.info("Found %d samples", num_samples)

        return dataset_type, num_samples, classes


class CityscapesDataset(FiftyOneDataset):
    """Cityscapes is a large-scale dataset that contains a diverse set of
    stereo video sequences recorded in street scenes from 50 different cities,
    with high quality pixel-level annotations of 5,000 frames in addition to a
    arger set of 20,000 weakly annotated frames.

    The dataset is intended for:

    -   assessing the performance of vision algorithms for major tasks of
    semantic urban scene understanding: pixel-level, instance-level, and
    panoptic semantic labeling
    -   supporting research that aims to exploit large volumes of (weakly)
    annotated data, e.g. for training deep neural networks

    Dataset size:
        11.8 GB

    Source:
        https://www.cityscapes-dataset.com

    Args:
        fine_annos (False): whether to load the fine annotations
        coarse_annos (False): whether to load the coarse annotations
        person_annos (False): whether to load the person annotations
    """

    def __init__(
        self, fine_annos=False, coarse_annos=False, person_annos=False
    ):
        self.fine_annos = fine_annos
        self.coarse_annos = coarse_annos
        self.person_annos = person_annos

    @property
    def name(self):
        return "cityscapes"

    @property
    def supported_splits(self):
        return ("train", "test", "validation")

    def _download_and_prepare(self, dataset_dir, scratch_dir, split):
        #
        # Cityscapes is distributed as a single download that contains all
        # splits (which must be manually downloaded), so we remove the split
        # from `dataset_dir` and download the whole dataset (only if necessary)
        #
        dataset_dir = os.path.dirname(dataset_dir)  # remove split dir
        split_dir = os.path.join(dataset_dir, split)
        if not os.path.exists(split_dir):
            """
            foucs.parse_cityscapes_dataset(
                dataset_dir,
                scratch_dir,
                [split],
                fine_annos=self.fine_annos,
                coarse_annos=self.coarse_annos,
                person_annos=self.person_annos,
            )
            """

        # Get metadata
        logger.info("Parsing dataset metadata")
        dataset_type = fot.FiftyOneDataset()
        importer = foud.FiftyOneDatasetImporter
        classes = sorted(
            importer.get_classes(os.path.join(dataset_dir, "train"))
            + importer.get_classes(os.path.join(dataset_dir, "test"))
            + importer.get_classes(os.path.join(dataset_dir, "validation"))
        )
        num_samples = importer.get_num_samples(split_dir)
        logger.info("Found %d samples", num_samples)

        return dataset_type, num_samples, classes


class BDD100KDataset(FiftyOneDataset):
    """The Berkeley Deep Drive (BDD) dataset is one of the largest and most
    diverese video datasets for autonomous vehicles.

    The BDD100k dataset contains 100,000 video clips collected from more than
    50,000 rides covering New York, San Francisco Bay Area, and other regions.
    The dataset contains diverse scene types such as city streets, residential
    areas, and highways. Furthermore, the videos were recorded in diverse
    weather conditions at different times of the day.

    The videos are split into training (70K), validation (10K) and testing
    (20K) sets. Each video is 40 seconds long with 720p resolution and a frame
    rate of 30fps. The frame at the 10th second of each video is annotated for
    image classification, detection, and segmentation tasks.

    This version of the dataset contains only the 100K images extracted from
    the videos as described above, together with the image classification,
    detection, and segmentation labels.

    **Manual download instructions**

    This dataset requires you to download the source data manually. You must
    register at https://bdd-data.berkeley.edu/ in order to get the link to
    download the dataset.

    After extracting the download, you will find contents similar to::

        bdd100k/
            labels/
                bdd100k_labels_images_train.json
                bdd100k_labels_images_val.json
            images/
                100k/
                    train/
                    test/
                    val/
            ...

    You must provide the path to the above ``bdd100k/`` folder when loading
    this dataset.

    Dataset size:
        7.1GB

    Source:
        https://bdd-data.berkeley.edu

    Args:
        source_dir (None): the path to the downloaded ``bdd100k/`` folder on
            disk
        copy_files (True): whether to move (False) or create copies (True) of
            the source files when populating the dataset directory
    """

    def __init__(self, source_dir=None, copy_files=True):
        self.source_dir = source_dir
        self.copy_files = copy_files

    @property
    def name(self):
        return "bdd100k"

    @property
    def supported_splits(self):
        return ("train", "validation", "test")

    def _download_and_prepare(self, dataset_dir, scratch_dir, split):
        #
        # BDD100k must be manually downloaded by the user and placed in
        # `self.source_dir` or `scratch_dir`
        #
        # The download contains all splits, so we remove the split from
        # `dataset_dir` and download the whole
        # dataset (only if necessary)
        #
        dataset_dir = os.path.dirname(dataset_dir)  # remove split dir
        split_dir = os.path.join(dataset_dir, split)
        if not os.path.exists(split_dir):
            bdd100k_dir = self.source_dir or scratch_dir
            foub.wrangle_bdd100k_download(
                bdd100k_dir, dataset_dir, copy_files=self.copy_files
            )

        # Get metadata
        logger.info("Parsing dataset metadata")
        dataset_type = fot.BDDDataset()
        num_samples = foub.BDDDatasetImporter.get_num_samples(split_dir)
        logger.info("Found %d samples", num_samples)

        return dataset_type, num_samples, None


class HMDB51Dataset(FiftyOneDataset):
    """HMDB51 is an action recognition dataset containing a total of 6,766
    clips distributed across 51 action classes.

    Dataset size:
        2.16 GB

    Source:
        https://serre-lab.clps.brown.edu/resource/hmdb-a-large-human-motion-database

    Args:
        fold (1): the test/train fold to use to arrange the files on disk. The
            supported values are ``(1, 2, 3)``
    """

    def __init__(self, fold=1):
        self.fold = fold

    @property
    def name(self):
        return "hmdb51"

    @property
    def parameters(self):
        return {"fold": self.fold}

    @property
    def supported_splits(self):
        return ("train", "test", "other")

    def _download_and_prepare(self, dataset_dir, scratch_dir, split):
        #
        # HMDB51 is distributed as a single download that contains all splits,
        # so we remove the split from `dataset_dir` and download the whole
        # dataset (only if necessary)
        #
        dataset_dir = os.path.dirname(dataset_dir)  # remove split dir
        split_dir = os.path.join(dataset_dir, split)
        if not os.path.exists(split_dir):
            fouh.download_hmdb51_dataset(
                dataset_dir,
                scratch_dir=scratch_dir,
                fold=self.fold,
                cleanup=False,
            )

        # Get metadata
        logger.info("Parsing dataset metadata")
        dataset_type = fot.VideoClassificationDirectoryTree()
        importer = foud.VideoClassificationDirectoryTreeImporter
        classes = importer.get_classes(split_dir)
        num_samples = importer.get_num_samples(split_dir)
        logger.info("Found %d samples", num_samples)

        return dataset_type, num_samples, classes


class UCF101Dataset(FiftyOneDataset):
    """UCF101 is an action recognition data set of realistic action videos,
    collected from YouTube, having 101 action categories. This data set is an
    extension of UCF50 data set which has 50 action categories.

    With 13,320 videos from 101 action categories, UCF101 gives the largest
    diversity in terms of actions and with the presence of large variations in
    camera motion, object appearance and pose, object scale, viewpoint,
    cluttered background, illumination conditions, etc, it is the most
    challenging data set to date. As most of the available action recognition
    data sets are not realistic and are staged by actors, UCF101 aims to
    encourage further research into action recognition by learning and
    exploring new realistic action categories.

    The videos in 101 action categories are grouped into 25 groups, where each
    group can consist of 4-7 videos of an action. The videos from the same
    group may share some common features, such as similar background, similar
    viewpoint, etc.

    Dataset size:
        6.48 GiB

    Source:
        https://www.crcv.ucf.edu/research/data-sets/ucf101

    Args:
        fold (1): the test/train fold to use to arrange the files on disk. The
            supported values are ``(1, 2, 3)``
    """

    def __init__(self, fold=1):
        self.fold = fold

    @property
    def name(self):
        return "ucf101"

    @property
    def parameters(self):
        return {"fold": self.fold}

    @property
    def supported_splits(self):
        return ("train", "test")

    def _download_and_prepare(self, dataset_dir, scratch_dir, split):
        #
        # UCF101 is distributed as a single download that contains all splits,
        # so we remove the split from `dataset_dir` and download the whole
        # dataset (only if necessary)
        #
        dataset_dir = os.path.dirname(dataset_dir)  # remove split dir
        split_dir = os.path.join(dataset_dir, split)
        if not os.path.exists(split_dir):
            fouu.download_ucf101_dataset(
                dataset_dir,
                scratch_dir=scratch_dir,
                fold=self.fold,
                cleanup=False,
            )

        # Get metadata
        logger.info("Parsing dataset metadata")
        dataset_type = fot.VideoClassificationDirectoryTree()
        importer = foud.VideoClassificationDirectoryTreeImporter
        classes = importer.get_classes(split_dir)
        num_samples = importer.get_num_samples(split_dir)
        logger.info("Found %d samples", num_samples)

        return dataset_type, num_samples, classes


AVAILABLE_DATASETS = {
    "quickstart": QuickstartDataset,
    "quickstart-video": VideoQuickstartDataset,
    "coco-2014-segmentation": COCO2014Dataset,
    "coco-2017-segmentation": COCO2017Dataset,
    "lfw": LabeledFacesInTheWildDataset,
    "cityscapes": CityscapesDataset,
    "bdd100k": BDD100KDataset,
    "hmdb51": HMDB51Dataset,
    "ucf101": UCF101Dataset,
}


def _move_dir(src, dst):
    for f in os.listdir(src):
        shutil.move(os.path.join(src, f), dst)
