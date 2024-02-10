import Header, { SearchFormValues } from '@/components/Header/Header'
import Main from '@/components/Main/Main'
import { Suspense, useState } from 'react'

export const Home = () => {
	const [searchValues, setSearchValues] = useState<SearchFormValues>()

	return (
		<div>
			<Header onSubmit={setSearchValues} />

			<Suspense
				fallback={
					<div className='w-full h-full flex items-center justify-center flex-col'>
						<img
							src='/team.jpg'
							alt='Loading'
							className='w-96 h-96 mt-10'
						/>
						<p className='text-2xl font-bold mt-8'>
							Please wait for our scraping team to collect the
							data...
						</p>
					</div>
				}
			>
				<Main searchValues={searchValues} />
			</Suspense>
		</div>
	)
}
