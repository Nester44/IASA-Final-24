import { Analytics } from '@/lib/api/fetchAnalytics'
import Sentiments from './Sentiments'

type Props = {} & Analytics

const Charts = ({ total_negatives, total_neutral, total_positives }: Props) => {
	return (
		<Sentiments
			total_negatives={total_negatives}
			total_neutral={total_neutral}
			total_positives={total_positives}
		/>
	)
}

export default Charts
