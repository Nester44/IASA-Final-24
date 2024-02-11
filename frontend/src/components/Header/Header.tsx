import { useForm } from 'react-hook-form'
import { Button } from '../ui/button'
import { Input } from '../ui/input'

import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Checkbox } from '../ui/checkbox'
import { Form, FormField, FormItem } from '../ui/form'
import { Label } from '../ui/label'
import { ScrollArea, ScrollBar } from '../ui/scroll-area'
import { ToggleGroup, ToggleGroupItem } from '../ui/toggle-group'

export const sources = [
	{ id: 'twitter', name: 'Twitter', iconSrc: 'twitter.png' },
	{ id: 'mctoday', name: 'MC Today', iconSrc: 'mctoday.png' },
	{ id: 'bbc-news', name: 'BBC', iconSrc: 'bbc.jpeg' },
	{ id: 'cnn', name: 'CNN', iconSrc: 'cnn.png' },
	{ id: 'breitbart-news', name: 'Breitbart', iconSrc: 'breitbart.png' },
] as const

export type SourceId = typeof sources[number]['id']
export const sourceIds = sources.map((source) => source.id)

const formSchema = z.object({
	query: z.string().min(2, {
		message: 'Query must be at least 2 characters.',
	}),
	period: z.enum(['day', 'week', 'month']),
	sources: z
		.array(
			z.enum(['mctoday', 'bbc-news', 'cnn', 'twitter', 'breitbart-news']),
		)
		.refine((sources) => sources.length > 0, {
			message: 'At least one source must be selected.',
		}),
})

export type SearchFormValues = z.infer<typeof formSchema>

type Props = {
	onSubmit: (values: SearchFormValues) => void
}

const Header = ({ onSubmit }: Props) => {
	const form = useForm<SearchFormValues>({
		resolver: zodResolver(formSchema),
		defaultValues: {
			query: '',
			period: 'day',
			sources: ['mctoday', 'twitter'],
		},
	})

	return (
		<header className='px-8 pt-8 border-b-2'>
			<Form {...form}>
				<form
					onSubmit={form.handleSubmit(onSubmit)}
					className='md:max-w-[800px] flex flex-col mx-auto'
				>
					<div className='flex w-full space-x-4'>
						<FormField
							control={form.control}
							name='query'
							render={({ field }) => (
								<Input
									placeholder='Enter keyword or phrase'
									{...field}
								/>
							)}
						/>

						<FormField
							control={form.control}
							name='period'
							render={({ field }) => (
								<ToggleGroup
									type='single'
									className='border rounded-md'
									value={field.value}
									onValueChange={(value) => {
										if (value) field.onChange(value)
									}}
								>
									<ToggleGroupItem value='day'>
										Day
									</ToggleGroupItem>
									<ToggleGroupItem value='week'>
										Week
									</ToggleGroupItem>
									<ToggleGroupItem value='month'>
										Month
									</ToggleGroupItem>
								</ToggleGroup>
							)}
						/>

						<Button type='submit'>Search</Button>
					</div>

					<ScrollArea className='w-full whitespace-nowrap py-6'>
						<div className='flex w-max space-x-4 m-auto'>
							{sources.map((source) => (
								<FormField
									key={source.id}
									control={form.control}
									name='sources'
									render={({ field }) => (
										<FormItem
											key={source.id}
											className='flex items-center space-x-2'
										>
											<Checkbox
												id={source.id}
												checked={field.value?.includes(
													source.id,
												)}
												onCheckedChange={(checked) => {
													return checked
														? field.onChange([
																...field.value,
																source.id,
														  ])
														: field.onChange(
																field.value?.filter(
																	(value) =>
																		value !==
																		source.id,
																),
														  )
												}}
											/>

											<Label
												htmlFor={source.id}
												className='flex items-center gap-2'
											>
												<img
													src={source.iconSrc}
													alt={source.name}
													className='w-8 h-8 rounded-sm'
												/>
												{source.name}
											</Label>
										</FormItem>
									)}
								/>
							))}
						</div>
						<ScrollBar orientation='horizontal' />
					</ScrollArea>
				</form>
			</Form>
		</header>
	)
}

export default Header
