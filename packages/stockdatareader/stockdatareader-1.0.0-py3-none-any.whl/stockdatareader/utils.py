import datetime
import stdnum.isin
import stdnum.cusip


def datestr_to_date(datestr):
    """Converts date string with format 'YYYY-MM-DD' into corresponding datetime.date object with format '%Y-%m-%d'.

    Parameters
    ----------
    datestr : str
        string containing the date in format "YYYY-MM-DD"

    Returns
    -------
    datetime.date

    """
    return datetime.datetime.strptime(datestr, '%Y-%m-%d').date()


def date_to_datestr(date):
    """Converts datetime.date object with format '%Y-%m-%d' into corresponding date string with format 'YYYY-MM-DD'.

    Parameters
    ----------
    date : datetime.date

    Returns
    -------
    str
        string containing the date in format "YYYY-MM-DD"

    """
    return str(date)


def to_date(date_):
    """Purifies to datetime.date object with format '%Y-%m-%d'

    Parameters
    ----------
    date_ : str or datetime.date

    Returns
    -------
    datetime.date

    """
    if type(date_) is datetime.date:
        return date_
    elif type(date_) is str:
        return datestr_to_date(date_)
    else:
        raise TypeError('argument must be datetime.date or str')


def to_datestr(date_):
    """Purifies to date string with format 'YYYY-MM-DD'

    Parameters
    ----------
    date_ : str or datetime.date

    Returns
    -------
    str
        String in the format 'YYYY-MM-DD'

    """
    if type(date_) is datetime.date:
        return date_to_datestr(date_)
    elif type(date_) is str:
        return date_
    else:
        raise TypeError('argument must be datetime.date or str')


def to_isin(stock_id):
    """Convert stock_id to ISIN

    Parameters
    ----------
    stock_id : str
        ISIN (International Securities Identification Number) or CUSIP

    Returns
    -------
    str
        ISIN

    """
    # Check if stock_id is ISIN
    if stdnum.isin.is_valid(stock_id):
        isin = stock_id
    else:
        # assume stock_is is CUSIP and convert to ISIN
        isin = stdnum.cusip.to_isin(stock_id)
    return isin


def find_nearest_date(items, pivot):
    """This function will return the datetime in items which is the closest to the date pivot.
    See https://stackoverflow.com/questions/32237862/find-the-closest-date-to-a-given-date

    Parameters
    ----------
    items : list
        List containing datetimes
    pivot : datetime.datime
        Datetime to be found

    Returns
    -------
    datetime.datetime

    """
    return min(items, key=lambda x: abs(x - pivot))
