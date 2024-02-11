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
		<div className='flex w-full'>
			<Sentiments
				total_negatives={total_negatives}
				total_neutral={total_neutral}
				total_positives={total_positives}
			/>

			<SourcesTrend posts={posts} />

			<PostsTrend posts={posts} />
		</div>
	)
}

export default Charts
