import { Post } from '@/lib/api/fetchAnalytics'
import PostCard from './PostCard'

type Props = {
	posts: Post[]
}

const Feed = ({ posts }: Props) => {
	return (
		<div className='grid md:grid-cols-2 lg:grid-cols-3 gap-4'>
			{posts.map((post) => (
				<PostCard key={post.id} {...post} />
			))}
		</div>
	)
}

export default Feed
