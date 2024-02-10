import { Post } from '@/lib/api/fetchAnalytics'

type Props = {
	posts: Post[]
}

const Feed = ({ posts }: Props) => {
	return (
		<div>
			{/* {posts.map((post) => (
				<PostCard {...post} />
			))} */}
		</div>
	)
}

export default Feed
