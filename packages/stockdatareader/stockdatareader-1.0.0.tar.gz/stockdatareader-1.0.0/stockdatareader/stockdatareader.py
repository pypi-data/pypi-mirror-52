import mechanicalsoup
import datetime
import pandas as pd
from io import StringIO

from . import utils


class StockDataReader:
    def __init__(self):
        self._browser = mechanicalsoup.StatefulBrowser(soup_config={'features': 'html5lib'})

    def read_data(self, stock_id, start_date, end_date):
        """Read historic stock data

        Parameters
        ----------
        stock_id : str
            ISIN (International Securities Identification Number) or CUSIP
        start_date : str or datetime.date
            Start date in format "YYYY-MM-DD"
        end_date : str or datetime.date
            End date in format "YYYY-MM-DD"

        Returns
        -------
        pandas.DataFrame
            DataFrame containing the stock data
            If any error occurs (e.g. no connection or stock not found) None is returned.

        """
        isin = utils.to_isin(stock_id)

        self._browser.open('https://www.ariva.de/'+isin+'/historische_kurse')

        try:
            form = self._browser.select_form(nr=2)  # returns the form of the part "Kurse als CSV-Datei"

            start_date = utils.to_datestr(start_date)
            end_date = utils.to_datestr(end_date)

            # convert date in format "YYYY-MM-DD" to format "DD-MM-YYYY"
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%d.%m.%Y')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%d.%m.%Y')

            # fill dates into form and submit
            form['min_time'] = start_date
            form['max_time'] = end_date
            response = self._browser.submit_selected()

        except Exception as e:
            print(e)
            return None

        # parse the response (content of the returned csv file) and store into pands.DataFrame
        # For use of StringIO in pd.read_csv see: https://stackoverflow.com/questions/22604564/how-to-create-a-pandas-dataframe-from-a-string # noqa
        data = StringIO(response.text)
        df = pd.read_csv(data, sep=';', thousands='.', decimal=',', index_col=0, skiprows=1, parse_dates=True,
                         dtype=float, names=['Open', 'High', 'Low', 'Close', 'Shares', 'Volume']
                         )

        # rename index column (contains dates) to 'Date'
        df.reset_index(level=0, inplace=True)
        df.rename(columns={'index': 'Date'}, inplace=True)

        return df

    def gain_over_time(self, stock_id, start_date, end_date):
        """Returns the gain over a time range

        Parameters
        ----------
        stock_id : str
            ISIN (International Securities Identification Number) or CUSIP
        start_date : str or datetime.date
            Start date in format "YYYY-MM-DD"
        end_date : str or datetime.date
            End date in format "YYYY-MM-DD"

        Returns
        -------
        float
            relative (w.r.t stock value at day of signal) and absolute gain or loss (negative number).
            None is returned if no data is available.

        """
        if utils.to_date(end_date) > datetime.datetime.today().date():
            return None  # if end_date is later than today

        stock_data = self.read_data(stock_id, start_date, end_date)
        if stock_data is None or stock_data.empty:
            return None
        start_value = stock_data['Close'].iloc[-1]
        stop_value = stock_data['Close'].iloc[0]
        absolute_gain = stop_value - start_value
        relative_gain = absolute_gain/start_value

        return relative_gain, absolute_gain
