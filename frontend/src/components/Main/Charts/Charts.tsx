import { Analytics } from '@/lib/api/fetchAnalytics'

import PostsTrend from './PostsTrend'
import Sentiments from './Sentiments'
import SourcesTrend from './SourcesTrend'

type Props = {} & Analytics

const Charts = ({
	total_negatives,
	total_neutral,
	total_positives,
	posts,
}: Props) => {
	return (
		<div className='w-full flex space-x-4'>
			<Sentiments
				total_negatives={total_negatives}
				total_neutral={total_neutral}
				total_positives={total_positives}
			/>

			<PostsTrend posts={posts} />
			<SourcesTrend posts={posts} />
		</div>
	)
}

export default Charts
