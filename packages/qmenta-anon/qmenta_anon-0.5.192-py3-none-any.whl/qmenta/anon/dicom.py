import logging
from datetime import datetime
import pydicom

from qmenta.anon.time_utils import TimeAnonymise


def PatchedMultiString(val, valtype=str):
    """
        Split a bytestring by delimiters if there are any
        val -- DICOM bytestring to split up
        valtype -- default str, but can be e.g. UID to overwrite to a specific type
    """
    # Remove trailing blank used to pad to even length
    # 2005.05.25: also check for trailing 0, error made in PET files we are converting

    if val and (val.endswith(' ') or val.endswith('\x00')):
        val = val[:-1]
    splitup = val.split("\\")
    if len(splitup) == 1:
        try:
            val = splitup[0]
            return valtype(val) if val else val
        except ValueError:
            if valtype is str or valtype is pydicom.valuerep.PersonName or valtype is pydicom.uid.UID:
                return valtype("XXXX") if val else val
            elif valtype is pydicom.valuerep.DSfloat:
                return valtype(0.0) if val else val
    else:
        return pydicom.multival.MultiValue(valtype, splitup)


# overwriting an existing method in order to prevent exceptions when
# tags annonymized with data of other type (e.g. float tag gets string)
pydicom.valuerep.MultiString = PatchedMultiString

# Basic Application Level Confidentiality Profile Attributes
# ftp://medical.nema.org/medical/dicom/final/sup55_ft.pdf

# The last two values for each element indicate the anonymisation type
# where the values have the following meanings:
# - 'X': Remove tag
# - 'Z': Replace with a zero length value, or a non-zero length value that
#       may be a dummy value and consistent with the Value Representations
# - 'D': Replace with a non-zero length value that may be a dummy value and
#       consistent with the Value Representations
# - 'A': Display exact age if <=89 years, and set to blank if >89 years


DICOM_ANON_MIN_SUPP_55 = [
    ("PatientName", (0x0010, 0x0010), "Z"),
    ("PatientID", (0x0010, 0x0020), "Z"),
    ("IssuerOfPatientID", (0x0010, 0x0021), "X"),
    ("PatientBirthTime", (0x0010, 0x0032), "X"),
    ("PatientSex", (0x0010, 0x0040), "Z"),
    ("PatientBirthName", (0x0010, 0x1005), "X"),
    ("CountryOfResidence", (0x0010, 0x2150), "X"),
    ("RegionOfResidence", (0x0010, 0x2152), "X"),
    ("PatientTelephoneNumbers", (0x0010, 0x2154), "X"),
    ("CurrentPatientLocation", (0x0038, 0x0300), "X"),
    ("PatientInstitutionResidence", (0x0038, 0x0400), "X"),
    ("StudyDate", (0x0008, 0x0020), "Z"),
    ("SeriesDate", (0x0008, 0x0021), "X"),
    ("AcquisitionDate", (0x0008, 0x0022), "X"),
    ("ContentDate", (0x0008, 0x0023), "Z"),
    ("OverlayDate", (0x0008, 0x0024), "X"),
    ("CurveDate", (0x0008, 0x0025), "X"),
    ("AcquisitionDateTime", (0x0008, 0x002A), "X"),
    ("StudyTime", (0x0008, 0x0030), "Z"),
    ("SeriesTime", (0x0008, 0x0031), "X"),
    ("AcquisitionTime", (0x0008, 0x0032), "X"),
    ("ContentTime", (0x0008, 0x0033), "Z"),
    ("OverlayTime", (0x0008, 0x0034), "X"),
    ("CurveTime", (0x0008, 0x0035), "X"),
    ("InstitutionAddress", (0x0008, 0x0081), "X"),
    ("ReferringPhysicianName", (0x0008, 0x0090), "Z"),
    ("ReferringPhysicianAddress", (0x0008, 0x0092), "X"),
    ("ReferringPhysicianTelephoneNumber", (0x0008, 0x0094), "X"),
    ("InstitutionalDepartmentName", (0x0008, 0x1040), "X"),
    ("OperatorsName", (0x0008, 0x1070), "X"),
    ("StudyID", (0x0020, 0x0010), "Z"),
    ("DateTime", (0x0040, 0xA120), "X"),
    ("Date", (0x0040, 0xA121), "X"),
    ("Time", (0x0040, 0xA122), "X"),
    ("PersonName", (0x0040, 0xA123), "D"),
    ("AccessionNumber", (0x0008, 0x0050), "Z"),
    ("InstitutionName", (0x0008, 0x0080), "X"),
    ("ReferringPhysicianIDSequence", (0x0008, 0x0096), "X"),
    ("PhysiciansOfRecord", (0x0008, 0x1048), "X"),
    ("PhysiciansOfRecordIDSequence", (0x0008, 0x1049), "X"),
    ("PerformingPhysicianName", (0x0008, 0x1050), "X"),
    ("PerformingPhysicianIDSequence", (0x0008, 0x1052), "X"),
    ("NameOfPhysicianReadingStudy", (0x0008, 0x1060), "X"),
    ("PhysicianReadingStudyIDSequence", (0x0008, 0x1062), "X"),
    ("PatientBirthDate", (0x0010, 0x0030), "Z"),
    ("PatientInsurancePlanCodeSequence", (0x0010, 0x0050), "X"),
    ("PatientPrimaryLanguageCodeSeq", (0x0010, 0x0101), "X"),
    ("OtherPatientIDs", (0x0010, 0x1000), "X"),
    ("OtherPatientNames", (0x0010, 0x1001), "X"),
    ("OtherPatientIDsSequence", (0x0010, 0x1002), "X"),
    ("PatientAge", (0x0010, 0x1010), "X"),
    ("PatientAddress", (0x0010, 0x1040), "X"),
    ("PatientMotherBirthName", (0x0010, 0x1060), "X")
]


def isstr(s):
    try:
        return isinstance(s, basestring)
    except NameError:
        return isinstance(s, str)


def redact_dicom_attr(header, tag):
    value = header[tag].value
    if isstr(value):
        header[tag].value = "XXXX"
    elif isinstance(value, pydicom.valuerep.PersonName) or isinstance(value, pydicom.valuerep.PersonName3):
        header[tag].value = "XXXX"
    elif isinstance(value, pydicom.valuerep.DSfloat):
        header[tag].value = 0.0
    elif isinstance(value, pydicom.uid.UID):
        header[tag].value = "XXXX"
    else:
        raise RuntimeError('Unknown type {} for tag {}'.format(type(value), tag))


def check_tag(header, tag):
    try:
        header[tag].value
        return True
    except (NotImplementedError, Exception):
        return False


def anonymise_header_tag(header, tagc):
    """
    Redact or delete the tag from the header as specified
    by the tag confidentiality setting. If the anonymisation action
    in tag is not in ["Z", "D", "X"], then no change will be applied.

    Parameters
    ----------
    header:
        The DICOM header to update

    tagc:
        The DICOM tag with its confidentiality in a tuple.
    """
    anonym_action = 2  # Only strong anonymisation
    if (tagc[anonym_action] != "") and check_tag(header, tagc[1]):
        if tagc[anonym_action] in ["Z", "D"]:
            redact_dicom_attr(header, tagc[1])
        elif tagc[anonym_action] == "X":
            try:
                del header[tagc[1]]
            except Exception:
                delattr(header, tagc[0])


def anonymise_dicom_dataset(dcm, cprof=DICOM_ANON_MIN_SUPP_55):
    """
    Anonyise the given DICOM header using the specified profile.

    Parameters
    ----------
    dcm:
        The DICOM header to anonymise

    cprof:
        The confidentiality profile to use when redacting the header.
        Default: DICOM_ANON_MIN_SUPP_55
    """
    logger = logging.getLogger(__name__)
    node_queue = [dcm]
    while node_queue:
        header = node_queue.pop(0)

        # anonymisation
        for tagc in cprof:
            anonymise_header_tag(header, tagc)

        # tail recursion
        for key in header.keys():
            if check_tag(header, key):
                elem = header[key]
                if isinstance(elem.value, pydicom.sequence.Sequence):
                    node_queue.extend(elem.value)
            else:
                template = "deleting key {!r} with invalid data from header when anonymising dicom file"
                logger.warning(template.format(key))
                try:
                    del header[key]
                except Exception:
                    delattr(header, key)


def anonymise(filename):
    header = pydicom.read_file(filename)

    anonymise_dicom_dataset(header, DICOM_ANON_MIN_SUPP_55)
    _updateUids(header)

    header.save_as(filename)
    return {"OK": True, "error_tags": []}


def _updateUids(header):
    """
    Update the relevant UID elements in the header.
    """
    for element in [2, 3, 0x10, 0x12]:
        if not check_tag(header, (2, element)):
            if element == 0x12:
                header.file_meta.ImplementationClassUID = "1.2.3.4"
            elif element == 2:
                header.file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
            elif element == 3:
                header.file_meta.MediaStorageSOPInstanceUID = "1.2.3"


def check_anonymised_file(input_file, options={}):
    _options = {
        "return_lines": False,
        "not_found_as_error": False
    }

    _options.update(options)

    lines = []
    not_anonymised_attr = []

    try:
        hd = pydicom.read_file(input_file)
        n_errors = 0
        for tag in DICOM_ANON_MIN_SUPP_55:
            if check_tag(hd, tag[1]):
                val = hd[tag[1]].value

                if _options["return_lines"]:
                    lines.append((tag[0], str(val)))

                try:
                    if not check_anonym_dicom_attr(hd, tag[1]):
                        not_anonymised_attr.append(tag[0])
                except Exception:
                    pass

            else:
                if _options["return_lines"]:
                    lines.append((tag[0], "!!!"))
                if _options["not_found_as_error"]:
                    n_errors += 1
    except Exception as e:
        return {"OK": False, "error": str(e)}

    ret = {"OK": True,
           "n_errors": n_errors,
           "not_anonymised_attr": not_anonymised_attr}

    if _options["return_lines"]:
        ret["lines"] = lines

    return ret


def check_anonym_dicom_attr(header, tag):
    value = header[tag].value
    if isstr(value):
        return str(header[tag].value) == "XXXX"
    elif isinstance(value, pydicom.valuerep.PersonName):
        return header[tag].value == "XXXX"
    elif isinstance(value, pydicom.valuerep.DSfloat):
        return header[tag].value == 0.0
    elif isinstance(value, pydicom.uid.UID):
        return header[tag].value == "XXXX"

    return True


class RelativeTimeAnonymiser:
    """
    Anonymise multiple DICOM files, while keeping the relative time/date
    differences for (AcquisitionDate, AcquisitionTime) and
    (ContentDate, ContentTime) tuples intact between all the files that
    are anonymised by the same instance of RelativeTimeAnonymiser.
    """

    # Extension of the explanation of the standard explained above
    # for DICOM_ANON_MIN_SUPP_55:
    # - 'R': Replace the date and time stored in the combination of these tags
    #        by a non-zero value that cannot be re-identified, but keep the
    #        relative times between different date/time tuples of different
    #        scans constant.
    #
    # When calling qmenta.anon.dicom.anonymise() or
    #   qmenta.anon.dicom.anonymise_dicom_dataset(), elements with the 'R' value
    #   are ignored because they 'R' is not in ['X', 'D', 'Z'].
    DICOM_KEEP_RELATIVE_TIME_OVERRIDE = [
        ("AcquisitionDate", (0x0008, 0x0022), "R"),
        ("AcquisitionTime", (0x0008, 0x0032), "R"),
        ("ContentDate", (0x0008, 0x0023), "R"),
        ("ContentTime", (0x0008, 0x0033), "R")
    ]

    @staticmethod
    def _replace_dicom_elements(original, override):
        """
        Returns a new list based on the original list, but with the elements
        where the first two parts of the tuple match the first two of the
        override list, the third value of that tuple is replaced by the third
        value of the tuple in the override list.
        """
        updated = []
        for v_orig in original:
            for v_repl in override:
                if (v_repl[0], v_repl[1]) == (v_orig[0], v_orig[1]):
                    updated.append(v_repl)
                    break
            else:
                # The inner loop was not broken
                updated.append(v_orig)

        return updated

    SUPP_55_RELATIVE_TIME = _replace_dicom_elements.__func__(
        DICOM_ANON_MIN_SUPP_55, DICOM_KEEP_RELATIVE_TIME_OVERRIDE
    )

    def __init__(self):
        self.time_anonymise = TimeAnonymise()

    @staticmethod
    def _time_to_TM(time):
        """
        See http://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_6.2.html
        """
        return '{:02}{:02}{:02}.{:06}'.format(
            time.hour, time.minute, time.second, time.microsecond
        )

    @staticmethod
    def _date_to_DA(date):
        """
        See http://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_6.2.html
        """
        return '{:04}{:02}{:02}'.format(date.year, date.month, date.day)

    @staticmethod
    def _tagc_from_cprof(cprof, tag):
        """
        Get the confidentiality profile setting for the specified tag.

        Parameters
        ----------
        cprof:
            The confidentiality profile

        tag: DICOM tag
            The tag of which we want to get the confidentiality profile setting

        Returns
        -------
        A tuple containing the DICOM tag with its confidentiality setting.

        Raises
        ------
        KeyError
            When the requested tag does not exist in the cprof
        """
        for tagc in cprof:
            if tagc[1] == tag:
                return tagc
        raise KeyError("Tag '{}' not found.".format(tag))

    def anonymise_datetime(self, header, cprof=DICOM_ANON_MIN_SUPP_55):
        """
        Anonymise the datetime values for AcquisitionDate, AcquisitionTime,
        ContentDate and ContentTime tags, while keeping the relative time
        differences of different dates/times for different calls of this
        function intact.

        Parameters
        ----------
        header:
            The DICOM header containing the datetime tags to anonymise

        cprof:
            The confidentiality profile that is used as a fallback when no
            pair of date, time can be found. In the case where only one of
            them exists, it will be anonymised as specified in the cprof.
            Default value: The original DICOM_ANON_MIN_SUPP_55.

        Raises
        ------
        time_utils.TooLargeDeltaError
            when trying to anonymise multiple DICOM headers of which the
            datetimes to anonymise span more than 24h.
        """
        datetime_tags = [
            # AcquisitionDate, AcquisitionTime:
            ((0x0008, 0x0022), (0x0008, 0x0032)),
            # ContentDate, ContentTime:
            ((0x0008, 0x0023), (0x0008, 0x0033))
        ]

        # Note: We currently do not support a single AquisitionDateTime or
        #   ContentDateTime tag. Two tags must be used to store date and time.

        for date_tag, time_tag in datetime_tags:
            date_ok = check_tag(header, date_tag)
            time_ok = check_tag(header, time_tag)
            if not (date_ok and time_ok):
                # A full datetime cannot be reconstructed. If one of the tags
                #   exists, anonymise it as specified in the original cprof to
                #   ensure proper anonymisation.
                if time_ok:
                    tagc = RelativeTimeAnonymiser._tagc_from_cprof(
                        DICOM_ANON_MIN_SUPP_55, time_tag)
                    anonymise_header_tag(header, tagc)
                elif date_ok:
                    tagc = RelativeTimeAnonymiser._tagc_from_cprof(
                        DICOM_ANON_MIN_SUPP_55, date_tag)
                    anonymise_header_tag(header, tagc)
                continue    # Go to the next (date, time) tag pair

            date_element = header[date_tag]
            time_element = header[time_tag]

            assert date_element.VR == 'DA'
            assert time_element.VR == 'TM'

            src_date = pydicom.valuerep.DA(date_element.value)
            src_time = pydicom.valuerep.TM(time_element.value)
            src_dt = datetime.combine(src_date, src_time)

            # Compute the target datetime
            tgt_dt = self.time_anonymise.anonymise_datetime(src_dt)

            header[date_tag].value = RelativeTimeAnonymiser._date_to_DA(tgt_dt)
            header[time_tag].value = RelativeTimeAnonymiser._time_to_TM(tgt_dt)

    def anonymise(self, filename):
        """
        Anonymise the DICOM dataset usinig the
        DICOM_SUPP_55_KEEP_RELATIVE_DATETIME profile, and replace
        the date/time elements with an anonymised date/time that keeps
        the relative date and time of different DICOM datasets intact.

        Parameters
        ----------
        filename: str
            The file to anonymise

        Raises
        ------
        time_utils.TooLargeDeltaError
            when trying to anonymise multiple DICOM headers of which the
            datetimes to anonymise span more than 24h.
        """
        header = pydicom.read_file(filename)

        self.anonymise_datetime(header)
        anonymise_dicom_dataset(header, RelativeTimeAnonymiser.SUPP_55_RELATIVE_TIME)
        _updateUids(header)

        header.save_as(filename)
