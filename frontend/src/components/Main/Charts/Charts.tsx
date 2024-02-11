import { Analytics } from '@/lib/api/fetchAnalytics'

import Cloud from './Cloud'
import PostsTrend from './PostsTrend'
import Sentiments from './Sentiments'
import SourcesTrend from './SourcesTrend'

type Props = {} & Analytics

const Charts = ({
	total_negatives,
	total_neutral,
	total_positives,
	posts,
	keywords,
}: Props) => {
	return (
		<div className='flex flex-col w-full mb-20'>
			<Cloud keywords={keywords} />
			<div className='w-full flex space-x-4'>
				<Sentiments
					total_negatives={total_negatives}
					total_neutral={total_neutral}
					total_positives={total_positives}
				/>

				<PostsTrend posts={posts} />
				<SourcesTrend posts={posts} />
			</div>
		</div>
	)
}

export default Charts
