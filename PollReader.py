import os
import unittest

class PollReader():
    """
    A class for reading and analyzing polling data.
    """
    def __init__(self, filename):
        self.base_path = os.path.abspath(os.path.dirname(__file__))
        self.full_path = os.path.join(self.base_path, filename)
        self.file_obj = open(self.full_path, 'r')
        self.raw_data = self.file_obj.readlines()
        self.file_obj.close()

        self.data_dict = {
            'month': [],
            'date': [],
            'sample': [],
            'sample type': [],
            'Harris result': [],
            'Trump result': []
        }

    def build_data_dict(self):
        # Skip header row
        for line in self.raw_data[1:]:
            parts = line.strip().split(',')
            if len(parts) != 5:
                continue  # skip malformed lines

            month = parts[0]
            date = int(parts[1])
            sample_info = parts[2].split()
            sample = int(sample_info[0])
            sample_type = sample_info[1]
            harris = float(parts[3])
            trump = float(parts[4])

            self.data_dict['month'].append(month)
            self.data_dict['date'].append(date)
            self.data_dict['sample'].append(sample)
            self.data_dict['sample type'].append(sample_type)
            self.data_dict['Harris result'].append(harris)
            self.data_dict['Trump result'].append(trump)

    def highest_polling_candidate(self):
        max_harris = max(self.data_dict['Harris result'])
        max_trump = max(self.data_dict['Trump result'])

        if max_harris > max_trump:
            return f"Harris: {max_harris:.1%}"
        elif max_trump > max_harris:
            return f"Trump: {max_trump:.1%}"
        else:
            return f"EVEN: {max_harris:.1%}"

    def likely_voter_polling_average(self):
        harris_total = 0
        trump_total = 0
        count = 0

        for i in range(len(self.data_dict['sample type'])):
            if self.data_dict['sample type'][i] == 'LV':
                harris_total += self.data_dict['Harris result'][i]
                trump_total += self.data_dict['Trump result'][i]
                count += 1

        harris_avg = harris_total / count
        trump_avg = trump_total / count
        return (harris_avg, trump_avg)

    def polling_history_change(self):
        harris_early = self.data_dict['Harris result'][:30]
        trump_early = self.data_dict['Trump result'][:30]
        harris_late = self.data_dict['Harris result'][-30:]
        trump_late = self.data_dict['Trump result'][-30:]

        harris_change = (sum(harris_late) / 30) - (sum(harris_early) / 30)
        trump_change = (sum(trump_late) / 30) - (sum(trump_early) / 30)

        return (harris_change, trump_change)

class TestPollReader(unittest.TestCase):
    def setUp(self):
        self.poll_reader = PollReader('polling_data.csv')
        self.poll_reader.build_data_dict()

    def test_build_data_dict(self):
        self.assertEqual(len(self.poll_reader.data_dict['date']), len(self.poll_reader.data_dict['sample']))
        self.assertTrue(all(isinstance(x, int) for x in self.poll_reader.data_dict['date']))
        self.assertTrue(all(isinstance(x, int) for x in self.poll_reader.data_dict['sample']))
        self.assertTrue(all(isinstance(x, str) for x in self.poll_reader.data_dict['sample type']))
        self.assertTrue(all(isinstance(x, float) for x in self.poll_reader.data_dict['Harris result']))
        self.assertTrue(all(isinstance(x, float) for x in self.poll_reader.data_dict['Trump result']))

    def test_highest_polling_candidate(self):
        result = self.poll_reader.highest_polling_candidate()
        self.assertTrue(isinstance(result, str))
        self.assertTrue("Harris" in result)
        self.assertTrue("57.0%" in result)

    def test_likely_voter_polling_average(self):
        harris_avg, trump_avg = self.poll_reader.likely_voter_polling_average()
        self.assertTrue(isinstance(harris_avg, float))
        self.assertTrue(isinstance(trump_avg, float))
        self.assertTrue(f"{harris_avg:.2%}" == "49.34%")
        self.assertTrue(f"{trump_avg:.2%}" == "46.04%")

    def test_polling_history_change(self):
        harris_change, trump_change = self.poll_reader.polling_history_change()
        self.assertTrue(isinstance(harris_change, float))
        self.assertTrue(isinstance(trump_change, float))
        self.assertTrue(f"{harris_change:+.2%}" == "+1.53%")
        self.assertTrue(f"{trump_change:+.2%}" == "+2.07%")

def main():
    poll_reader = PollReader('polling_data.csv')
    poll_reader.build_data_dict()

    highest_polling = poll_reader.highest_polling_candidate()
    print(f"Highest Polling Candidate: {highest_polling}")
    
    harris_avg, trump_avg = poll_reader.likely_voter_polling_average()
    print(f"Likely Voter Polling Average:")
    print(f"  Harris: {harris_avg:.2%}")
    print(f"  Trump: {trump_avg:.2%}")
    
    harris_change, trump_change = poll_reader.polling_history_change()
    print(f"Polling History Change:")
    print(f"  Harris: {harris_change:+.2%}")
    print(f"  Trump: {trump_change:+.2%}")

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)